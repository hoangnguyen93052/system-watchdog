import os
import subprocess
import json
import pefile
import hashlib
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BinaryAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.pe = None
        self.hashes = {}

    def analyze(self):
        self.pe = pefile.PE(self.file_path)
        self.hashes['md5'] = self.calculate_hash('md5')
        self.hashes['sha1'] = self.calculate_hash('sha1')
        self.hashes['sha256'] = self.calculate_hash('sha256')
        logger.info(f"Analyzed {self.file_path}: {self.hashes}")

    def calculate_hash(self, algo: str) -> str:
        hasher = hashlib.new(algo)
        with open(self.file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def get_imported_functions(self) -> List[str]:
        imports = []
        for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
            imports.append(entry.dll.decode('utf-8'))
            for func in entry.imports:
                imports.append(func.name.decode('utf-8') if func.name else None)
        return imports

    def get_exported_functions(self) -> List[str]:
        exports = []
        if hasattr(self.pe, 'DIRECTORY_ENTRY_EXPORT'):
            for export in self.pe.DIRECTORY_ENTRY_EXPORT.symbols:
                exports.append(export.name.decode('utf-8') if export.name else None)
        return exports

class CommandLineInterface:
    def __init__(self):
        self.commands = {
            'analyze': self.analyze,
            'imports': self.get_imports,
            'exports': self.get_exports,
            'exit': self.exit_cli
        }

    def start(self):
        while True:
            command = input("Enter command: ")
            if command in self.commands:
                self.commands[command]()
            else:
                logger.warning("Unknown command. Try again.")

    def analyze(self):
        file_path = input("Enter path to binary: ")
        analyzer = BinaryAnalyzer(file_path)
        analyzer.analyze()
        logger.info(f"Analysis complete for {file_path}")

    def get_imports(self):
        file_path = input("Enter path to binary: ")
        analyzer = BinaryAnalyzer(file_path)
        analyzer.analyze()
        imports = analyzer.get_imported_functions()
        logger.info(f"Imported functions: {imports}")

    def get_exports(self):
        file_path = input("Enter path to binary: ")
        analyzer = BinaryAnalyzer(file_path)
        analyzer.analyze()
        exports = analyzer.get_exported_functions()
        logger.info(f"Exported functions: {exports}")

    def exit_cli(self):
        logger.info("Exiting CLI.")
        exit(0)

def main():
    logger.info("Starting Reverse Engineering Tools.")
    cli = CommandLineInterface()
    cli.start()

if __name__ == "__main__":
    main()