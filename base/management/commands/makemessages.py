"""
Ensure PO files are generated using forward slashes in the location comments on all operating systems
"""
import os

from django.core.management.commands.makemessages import Command as MakeMessagesCommand


class Command(MakeMessagesCommand):
    def find_files(self, root):
        all_files = super().find_files(root)
        if os.sep != "\\":
            return all_files

        for file_entry in all_files:
            if file_entry.dirpath == ".":
                file_entry.dirpath = ""
            elif file_entry.dirpath.startswith(".\\"):
                file_entry.dirpath = file_entry.dirpath[2:].replace("\\", "/")

        return all_files

    def build_potfiles(self):
        pot_files = super().build_potfiles()
        if os.sep != "\\":
            return pot_files

        for filename in pot_files:
            lines = open(filename, "r", encoding="utf-8").readlines()
            fixed_lines = []
            for line in lines:
                if line.startswith("#: "):
                    line = line.replace("\\", "/")
                fixed_lines.append(line)

            with open(filename, "w", encoding="utf-8") as f:
                f.writelines(fixed_lines)

        return pot_files
