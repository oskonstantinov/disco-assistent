from prompt_toolkit import PromptSession
from typing import Optional, List
from processors.xml_processor import XMLStreamProcessor
from ui.renderer import DialogRenderer
from audio.sound_manager import SoundManager
import logging
from blessed import Terminal
from models.skill_check import SkillCheck
from models.context_update import ContextUpdate
import asyncio

class DialogStateManager:
    def __init__(self, config_manager=None):
        self.session = PromptSession()
        self.processor = XMLStreamProcessor()
        self.renderer = DialogRenderer(config_manager)
        self.sound_manager = SoundManager()
        self.term = Terminal()
        self._logger = logging.getLogger(__name__)
        self._current_check: Optional[SkillCheck] = None
        self._next_check: Optional[SkillCheck] = None
        self._waiting_for_continue = False
        self.config_manager = config_manager

    async def handle_user_input(self) -> Optional[str]:
        try:
            user_input = await self.session.prompt_async(">>> ")

            if user_input.lower() in ('exit', 'quit'):
                raise EOFError("Check failure: User requested exit")

            if not user_input or user_input.isspace():
                return None

            self.renderer.render_user_input(user_input)
            self.sound_manager.play_click()
            return user_input

        except (EOFError, KeyboardInterrupt):
            print(self.term.show_cursor, end='', flush=True)
            raise

    async def process_response_chunk(self, chunk: str) -> None:
        try:
            for item in self.processor.process_stream(chunk):
                if not item:
                    continue

                if isinstance(item, ContextUpdate):
                    # Handle context update
                    await self._handle_context_update(item)
                elif isinstance(item, SkillCheck):
                    # Handle skill check (existing logic)
                    if self._current_check is None:
                        self._current_check = item
                        self.renderer.render_skill_check(item, show_continue=True, continue_active=False)
                        if item.category:
                            self.sound_manager.play_skill_sound(item.category)
                    elif self._next_check is None:
                        self._next_check = item
                        self.renderer.update_continue(active=True)
                        self._waiting_for_continue = True
                        await self._wait_for_continue()
                    else:
                        while self._waiting_for_continue:
                            await asyncio.sleep(0.1)
                        self._current_check = item
                        self._next_check = None
                        self.renderer.render_skill_check(item, show_continue=True, continue_active=False)
                        if item.category:
                            self.sound_manager.play_skill_sound(item.category)

        except Exception as e:
            self._logger.error(f"Check failure: Error processing chunk: {e}")

    async def _handle_context_update(self, context_update: ContextUpdate) -> None:
        """Handle context update by appending to user_context.txt and generating a response."""
        try:
            # Append to user_context.txt
            context_file_path = "config/user_context.txt"
            with open(context_file_path, 'a', encoding='utf-8') as f:
                f.write(f"\n{context_update.content}\n")
            
            self._logger.info(f"Context updated with: {context_update.content}")
            
            # Create a skill check response to inform the user
            # Use Encyclopedia as it's the skill that represents knowledge and learning
            from models.skill_check import SkillCheck
            
            # Get the language for the notification
            language = self.config_manager.get_language() if self.config_manager else 'en'
            
            if language == 'ru':
                context_notification = f"Новая информация добавлена в память: {context_update.content}"
            else:
                context_notification = f"New information added to memory: {context_update.content}"
            
            notification_check = SkillCheck(
                skill="Encyclopedia",
                difficulty="Medium",
                success=True,
                content=context_notification,
                category="INTELLECT"
            )
            
            # Render the notification
            if self._current_check is None:
                self._current_check = notification_check
                self.renderer.render_skill_check(notification_check, show_continue=True, continue_active=False)
                self.sound_manager.play_skill_sound("INTELLECT")
            elif self._next_check is None:
                self._next_check = notification_check
                self.renderer.update_continue(active=True)
                self._waiting_for_continue = True
                await self._wait_for_continue()
                
        except Exception as e:
            self._logger.error(f"Check failure: Error handling context update: {e}")

    async def _wait_for_continue(self) -> None:
        if not self._waiting_for_continue:
            return

        try:
            await self.session.prompt_async("", refresh_interval=None)
            self.renderer.clear_continue()
            self.sound_manager.play_click()

            if self._next_check:
                self._current_check = self._next_check
                self._next_check = None
                self.renderer.render_skill_check(self._current_check, show_continue=True, continue_active=False)
                if self._current_check.category:
                    self.sound_manager.play_skill_sound(self._current_check.category)

            self._waiting_for_continue = False

        except Exception as e:
            self._logger.error(f"Check failure: Error waiting for continue: {e}")

    async def finish_response(self) -> None:
        try:
            remaining_items = list(self.processor.process_stream(self.processor.get_remaining_buffer()))

            for item in remaining_items:
                if isinstance(item, ContextUpdate):
                    await self._handle_context_update(item)
                elif isinstance(item, SkillCheck):
                    if self._current_check is None:
                        self._current_check = item
                        self.renderer.render_skill_check(item, show_continue=False)
                        if item.category:
                            self.sound_manager.play_skill_sound(item.category)
                    else:
                        self._next_check = item
                        self.renderer.update_continue(active=True)
                        self._waiting_for_continue = True
                        await self._wait_for_continue()

            self.processor.clear_buffer()
            self._current_check = None
            self._next_check = None
            self._waiting_for_continue = False
            self.renderer.clear_continue()

        except Exception as e:
            self._logger.error(f"Check failure: Error processing final chunk: {e}")
