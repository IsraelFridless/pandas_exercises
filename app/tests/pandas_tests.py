def test_dataframe(students):
    students_copy = students.copy()
    students_copy['Age_Group'] = students_copy['Age'].apply(lambda age: 'Old' if age > 21 else 'Young')
    print(students_copy.iloc[:, [0, -1]])

def test_create_language_category(students):
    compiled_langs = {'Java', 'C#', 'C++', 'Rust', 'Swift', 'Go', 'Kotlin'}
    students_copy = students.copy()
    students_copy['Language_Type'] = students_copy['Favorite_Language'].apply(lambda language: 'Compiled' if language in compiled_langs else 'Interpreter')
    print(students_copy.iloc[:, [0, -1]])



