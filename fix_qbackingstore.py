import os
import re

APP_DIR = r"e:\FluentUI\app"

OVERLAY_FILES = {
    "fluent_toast.py",
    "fluent_notification.py",
    "fluent_positional_notification.py",
    "fluent_popover.py",
    "fluent_tooltip.py",
    "fluent_drawer.py",
    "fluent_dialog.py",
    "fluent_user_info_overlay.py",
    "fluent_popconfirm.py",
    "fluent_tour.py",
    "fluent_loading_screen.py",
}

def is_overlay(filepath):
    return os.path.basename(filepath) in OVERLAY_FILES

def find_py_files(directory):
    py_files = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.join(root, f))
    return py_files

def has_fillrect_transparent(content):
    return bool(re.search(r'painter\.fillRect\(self\.rect\(\),\s*Qt\.transparent\)', content))

def has_wa_translucent(content):
    return bool(re.search(r'self\.setAttribute\(Qt\.WA_TranslucentBackground\)', content))

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    overlay = is_overlay(filepath)
    changes = []

    if has_fillrect_transparent(content):
        fill_rect_pattern = re.compile(
            r'^([ \t]*)painter\.fillRect\(self\.rect\(\),\s*Qt\.transparent\)\s*\n',
            re.MULTILINE
        )

        matches = list(fill_rect_pattern.finditer(content))
        if matches:
            if overlay:
                for m in reversed(matches):
                    content = content[:m.start()] + content[m.end():]
                changes.append("Removed fillRect(Qt.transparent) [overlay - keeps WA_TranslucentBackground]")
            else:
                for m in reversed(matches):
                    indent = m.group(1)
                    replacement = f"{indent}painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))\n"
                    content = content[:m.start()] + replacement + content[m.end():]
                changes.append("Replaced fillRect(Qt.transparent) with fillRect(QColor(tm.color('bg_solid_card')))")

    if has_wa_translucent(content) and not overlay:
        wa_pattern = re.compile(
            r'^[ \t]*self\.setAttribute\(Qt\.WA_TranslucentBackground\)\s*\n',
            re.MULTILINE
        )
        content = wa_pattern.sub('', content)
        changes.append("Removed setAttribute(Qt.WA_TranslucentBackground)")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return changes
    return None

py_files = find_py_files(APP_DIR)

modified = []
for filepath in sorted(py_files):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if not has_fillrect_transparent(content) and not has_wa_translucent(content):
        continue
    changes = fix_file(filepath)
    if changes:
        rel = os.path.relpath(filepath, APP_DIR)
        modified.append((rel, changes))
        print(f"FIXED: {rel}")
        for c in changes:
            print(f"  - {c}")

print(f"\n=== SUMMARY ===")
print(f"Total files scanned: {len(py_files)}")
print(f"Files modified: {len(modified)}")
for rel, changes in modified:
    print(f"\n{rel}:")
    for c in changes:
        print(f"  - {c}")
