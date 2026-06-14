import re, sys
with open('index.html', encoding='utf-8') as f:
    html = f.read()

errors = []

# 1. Check no broken Arabic (mojibake)
if 'O\x15' in html or '\u0000' in html:
    errors.append('MOJIBAKE Arabic characters found')

# 2. All key DOM IDs present
for id_ in ['sidebar','topbar','contentScroll','page-dashboard','page-lecture','page-final_exam',
            'dashGrid','lecTitle','lecContent','lecNotes','lecConcepts','lecExamNotes',
            'lecFlashcards','lecQuizBox','lecExpected','finalQuizBox','timerModal','timerDisplay']:
    if f'id="{id_}"' not in html:
        errors.append(f'MISSING id: {id_}')

# 3. Check JS functions exist
for fn in ['init','buildSidebar','showPage','loadLecture','buildQuiz','gradeQuiz','buildFinalExam',
           'selectOpt','toggleTheme','toggleLang','openSidebar','closeSidebar','toggleTimer','buildDashboard']:
    if f'function {fn}' not in html:
        errors.append(f'MISSING function: {fn}')

# 4. No raw %s placeholder left
if '%s' in html:
    errors.append('Unresolved placeholder found')

# 5. DATABASE present
if 'const DB = [' not in html:
    errors.append('DB variable not found')

# 6. No DATABASE_PLACEHOLDER left
if 'DATABASE_PLACEHOLDER' in html:
    errors.append('DATABASE_PLACEHOLDER was not replaced')

# 7. Count lectures in DB
import json
start = html.index('const DB = [') + len('const DB = ')
# find matching bracket
depth = 0
end = start
for i, c in enumerate(html[start:], start):
    if c == '[': depth += 1
    elif c == ']':
        depth -= 1
        if depth == 0:
            end = i + 1
            break
db = json.loads(html[start:end])
if len(db) != 4:
    errors.append(f'DB has {len(db)} lectures, expected 4')

# 8. Check Arabic in DB
for lec in db:
    if not lec.get('title_ar'):
        errors.append(f'Missing Arabic title for {lec["id"]}')
    if not lec.get('content_ar'):
        errors.append(f'Missing Arabic content for {lec["id"]}')

print(f'File size: {len(html):,} chars')
print(f'Lectures in DB: {len(db)}')
for lec in db:
    q_count = len(lec['quizzes'].get('mcq',[])) + len(lec['quizzes'].get('tf',[])) + len(lec['quizzes'].get('definitions',[])) + len(lec['quizzes'].get('short_answer',[]))
    fc_count = len(lec['flashcards'])
    eq_count = len(lec['expected_questions'])
    print(f"  {lec['id']}: {q_count} quiz Qs, {fc_count} flashcards, {eq_count} expected Qs")

if errors:
    print()
    for e in errors:
        print('ERROR:', e)
    sys.exit(1)
else:
    print()
    print('ALL CHECKS PASSED - Zero errors detected')
