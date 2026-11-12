"""Optional local Tesseract OCR adapter for raster invoice images.

The adapter invokes the Tesseract CLI without a shell, sends bytes over stdin,
and never writes the source document to disk.
"""
from __future__ import annotations

import csv
import io
import subprocess
from collections import OrderedDict
from dataclasses import dataclass

from fatora.adapters import OCRCapabilities, OCRResult, TextBlock
from fatora.documents import DocumentInput


@dataclass(frozen=True, slots=True)
class TesseractAdapter:
    """Run a locally installed Tesseract binary against supported raster images."""

    executable: str = "tesseract"
    languages: str = "ara+eng"
    timeout_seconds: float = 30.0

    @property
    def name(self) -> str:
        return "tesseract"

    @property
    def capabilities(self) -> OCRCapabilities:
        return OCRCapabilities(
            media_types=("image/png", "image/jpeg", "image/tiff"),
            languages=tuple(self.languages.split("+")),
            supports_layout=False,
            supports_tables=False,
        )

    def extract(self, document: DocumentInput) -> OCRResult:
        """Return line-level OCR blocks with page and mean word confidence."""
        if document.media_type not in self.capabilities.media_types:
            raise ValueError(
                f"Tesseract adapter does not support {document.media_type!r}."
            )
        try:
            completed = subprocess.run(
                [
                    self.executable,
                    "stdin",
                    "stdout",
                    "-l",
                    self.languages,
                    "tsv",
                ],
                input=document.content,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                timeout=self.timeout_seconds,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                "Tesseract executable was not found. Install Tesseract and its language data."
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("Tesseract OCR exceeded its configured time limit.") from exc
        except OSError as exc:
            raise RuntimeError("Tesseract could not be started.") from exc

        if completed.returncode != 0:
            raise RuntimeError(
                "Tesseract OCR failed. Check the local installation and requested language data."
            )

        try:
            rows = csv.DictReader(
                io.StringIO(completed.stdout.decode("utf-8-sig")),
                delimiter="\t",
            )
            grouped: OrderedDict[tuple[int, int, int, int], list[tuple[int, str, float]]] = (
                OrderedDict()
            )
            for row in rows:
                if row.get("level") != "5":
                    continue
                text = (row.get("text") or "").strip()
                if not text:
                    continue
                try:
                    page = int(row["page_num"])
                    block = int(row["block_num"])
                    paragraph = int(row["par_num"])
                    line = int(row["line_num"])
                    word = int(row["word_num"])
                    confidence = float(row["conf"])
                except (KeyError, TypeError, ValueError) as exc:
                    raise RuntimeError("Tesseract returned malformed TSV output.") from exc
                if confidence < 0:
                    continue
                key = (page, block, paragraph, line)
                grouped.setdefault(key, []).append((word, text, confidence))
        except UnicodeDecodeError as exc:
            raise RuntimeError("Tesseract returned non-UTF-8 TSV output.") from exc

        blocks = []
        for (page, _block, _paragraph, _line), words in grouped.items():
            words.sort(key=lambda item: item[0])
            line_text = " ".join(item[1] for item in words)
            mean_confidence = sum(item[2] for item in words) / len(words) / 100
            blocks.append(
                TextBlock(
                    text=line_text,
                    page=page,
                    confidence=max(0.0, min(1.0, mean_confidence)),
                )
            )

        return OCRResult(
            blocks=tuple(blocks),
            provider=self.name,
            metadata={
                "languages": self.languages,
                "input_media_type": document.media_type,
                "block_granularity": "line",
            },
        )
