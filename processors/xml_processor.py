from typing import Optional, Generator, Union
import xml.etree.ElementTree as ET
from models.skill_check import SkillCheck
from models.context_update import ContextUpdate
from config.constants import SKILL_CATEGORIES
from utils.exceptions import XMLProcessingError
from localization.translations import TRANSLATIONS
import logging

class XMLStreamProcessor:
    def __init__(self):
        self.buffer = ""
        self._logger = logging.getLogger(__name__)
        self._partial_tag = ""

    def _normalize_text(self, text: str) -> str:
        dashes = ['—', '–', '‐', '‑', '⁃', '−']
        for dash in dashes:
            text = text.replace(dash, '-')
        return ' '.join(text.split())

    def clear_buffer(self) -> None:
        self.buffer = ""

    def process_stream(self, chunk: str) -> Generator[Optional[Union[SkillCheck, ContextUpdate]], None, None]:
        if hasattr(chunk, 'text'):
            chunk = chunk.text
        elif isinstance(chunk, list) and len(chunk) > 0 and hasattr(chunk[0], 'text'):
            chunk = chunk[0].text

        chunk = str(chunk)
        self.buffer += chunk

        while True:
            # Check for skill tags first
            start = self.buffer.find("<skill")
            if start != -1:
                end = self.buffer.find("</skill>", start)
                if end != -1:
                    end += len("</skill>")
                    complete_tag = self.buffer[start:end]
                    try:
                        skill_check = self._parse_skill_check(complete_tag)
                        if skill_check:
                            yield skill_check
                        self.buffer = self.buffer[end:]
                        continue
                    except ET.ParseError as e:
                        self._logger.debug(f"Partial XML chunk received: {complete_tag}")
                        break
                    except Exception as e:
                        self._logger.error(f"Check failure: Error processing XML chunk: {e}")
                        self.buffer = self.buffer[end:]
                        continue
            
            # Check for context_update tags
            start = self.buffer.find("<context_update")
            if start != -1:
                end = self.buffer.find("</context_update>", start)
                if end != -1:
                    end += len("</context_update>")
                    complete_tag = self.buffer[start:end]
                    try:
                        context_update = self._parse_context_update(complete_tag)
                        if context_update:
                            yield context_update
                        self.buffer = self.buffer[end:]
                        continue
                    except ET.ParseError as e:
                        self._logger.debug(f"Partial XML chunk received: {complete_tag}")
                        break
                    except Exception as e:
                        self._logger.error(f"Check failure: Error processing context update: {e}")
                        self.buffer = self.buffer[end:]
                        continue
            
            # No complete tags found
            break

    def _normalize_skill_name(self, skill_name: str) -> str:
        skill_name = skill_name.strip()
        ru_skills = TRANSLATIONS.get('ru', {}).get('skills', {})
        for category, skills in SKILL_CATEGORIES.items():
            for skill in skills:
                if skill_name.lower() == skill.lower() or skill_name.lower() == ru_skills.get(skill, '').lower():
                    return skill
        return skill_name

    def _normalize_difficulty(self, difficulty: str) -> str:
        from config.constants import DIFFICULTY_LEVELS
        difficulty = difficulty.strip()
        for level in DIFFICULTY_LEVELS.keys():
            if difficulty.lower() == level.lower():
                return level
        return difficulty

    def _parse_skill_check(self, xml_chunk: str) -> Optional[SkillCheck]:
        try:
            root = ET.fromstring(xml_chunk)

            raw_skill_name = root.attrib.get('name', 'Unknown')
            skill_name = self._normalize_skill_name(raw_skill_name)

            raw_difficulty = root.attrib.get('difficulty', 'medium')
            difficulty = self._normalize_difficulty(raw_difficulty)

            success = root.attrib.get('success', 'false').lower() == 'true'
            content = self._normalize_text(root.text or "")

            category = next(
                (cat for cat, skills in SKILL_CATEGORIES.items()
                 if skill_name in skills),
                None
            )

            return SkillCheck(
                skill=skill_name,
                difficulty=difficulty,
                success=success,
                content=content,
                category=category
            )
        except ET.ParseError as e:
            raise
        except Exception as e:
            self._logger.error(f"Check failure: Error parsing skill check: {e}")
            return None

    def _parse_context_update(self, xml_chunk: str) -> Optional[ContextUpdate]:
        try:
            root = ET.fromstring(xml_chunk)
            content = self._normalize_text(root.text or "")
            
            if content.strip():
                return ContextUpdate(content=content)
            return None
        except ET.ParseError as e:
            raise
        except Exception as e:
            self._logger.error(f"Error parsing context update: {e}")
            return None

    def get_remaining_buffer(self) -> str:
        return self.buffer
