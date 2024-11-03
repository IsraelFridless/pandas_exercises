from functools import reduce

import pandas as pd

# Exercise 1: Find all courses taught by Dr. Enosh Tsur
def test_find_enosh(courses):
    by_enosh = courses[courses['Instructor'] == 'Dr. Enosh Tsur']
    # Assert the number of courses he teaches
    assert len(by_enosh) == 2

    # Assert the specific courses he teaches
    assert (set(by_enosh['Course_Name'].values) ==
            {'Database Systems', 'Data Science Fundamentals'})

    # Assert the departments he teaches in
    assert (set(by_enosh['Department'].values) ==
            {'Computer Science', 'Data Science'})

    # Assert course IDs
    assert (set(by_enosh['Course_ID'].values) ==
            {'CS301', 'DS101'})

    # Assert all rows have the correct instructor
    assert all(
        instructor == 'Dr. Enosh Tsur'
        for instructor in by_enosh['Instructor']
    )

    # Assert the difficulty levels of his courses
    assert set(by_enosh['Difficulty_Level'].values) == {'Intermediate', 'Beginner'}

    # Assert the credits of his courses
    assert all(credit == 3 for credit in by_enosh['Credits'])


# Exercise 2: Count how many courses are there per department
def test_count_courses_per_department(courses):
    dept_counts = courses['Department'].value_counts()

    # Assert total number of courses
    assert len(courses) == 10

    # Assert specific department counts
    assert dept_counts['Computer Science'] == 5
    assert dept_counts['Web Development'] == 3
    assert dept_counts['Data Science'] == 2

    # Assert these are all the departments
    assert set(dept_counts.index) == {'Computer Science', 'Web Development', 'Data Science'}

# Exercise 3: Calculate average credits for each difficulty level
def test_average_credits_by_difficulty(courses):
    # The original data might look like this:
    """
    Difficulty_Level    Credits
    Beginner           3
    Beginner           3
    Beginner           3
    Intermediate       3
    Intermediate       4
    Intermediate       3
    Advanced           4
    Advanced           4
    """

    # After groupby('Difficulty_Level'), you have three groups:
    """
    Beginner group: [3, 3, 3]
    Intermediate group: [3, 4, 3]
    Advanced group: [4, 4]
    """

    # After .mean(), you get:
    """
    Difficulty_Level
    Beginner       3.0
    Intermediate   3.5
    Advanced       4.0
    """
    avg_credits = courses.groupby('Difficulty_Level')['Credits'].mean()
    print(avg_credits)

    # Assert average credits for each level
    assert avg_credits['Beginner'] == 3.0
    assert avg_credits['Intermediate'] == 3.5
    assert avg_credits['Advanced'] == 4.0

    # Assert we have all difficulty levels
    assert set(avg_credits.index) == {'Beginner', 'Intermediate', 'Advanced'}


# Exercise 4: Find and sort beginner courses
def test_sorted_beginner_courses(courses):
    beginner_courses = courses[
        courses['Difficulty_Level'] == 'Beginner'
        ].sort_values('Course_Name')


    # Assert number of beginner courses
    assert len(beginner_courses) == 3

    # Assert course names are in correct order
    assert list(beginner_courses['Course_Name']) == [
        'Data Science Fundamentals',
        'Introduction to Programming',
        'Web Development Basics'
    ]

    # Assert all are actually beginner courses
    assert all(
        level == 'Beginner'
        for level in beginner_courses['Difficulty_Level']
    )

# Exercise 5: Test pivot table of department and difficulty
def test_difficulty_by_department(courses):
    pivot = pd.pivot_table(
        courses,  # DataFrame to pivot
        index='Department',  # Rows
        columns='Difficulty_Level',  # Columns
        aggfunc='size',  # What to calculate (here: count)
        fill_value=0  # Replace NaN with 0
    )

    print(pivot)

    # Assert Computer Science department counts
    assert pivot.loc['Computer Science', 'Beginner'] == 1
    assert pivot.loc['Computer Science', 'Intermediate'] == 2
    assert pivot.loc['Computer Science', 'Advanced'] == 2

    # Assert Web Development department counts
    assert pivot.loc['Web Development', 'Beginner'] == 1
    assert pivot.loc['Web Development', 'Intermediate'] == 1
    assert pivot.loc['Web Development', 'Advanced'] == 1

    # Assert Data Science department counts
    assert pivot.loc['Data Science', 'Beginner'] == 1
    assert pivot.loc['Data Science', 'Intermediate'] == 1
    assert pivot.loc['Data Science', 'Advanced'] == 0


def test_course_full_name(courses):
    courses['Full_Name'] = courses.apply(
        lambda row: f"{row['Course_ID']}: {row['Course_Name']}",
        axis=1
    )


# Add a new course "Mobile Development" with appropriate details like Course_ID, Department, etc.
def test_add_new_course(courses):
    new_course = [{
        'Course_ID': 'CS156',
        'Course_Name': 'Mobile Development',
        'Department': 'Web Development',
        'Credits': 2,
        'Instructor': 'Dr. Enosh Tsur',
        'Difficulty_Level': 'Intermediate'
    }]
    new_course_df = pd.DataFrame(new_course)
    courses = pd.concat([courses, new_course_df], ignore_index=True)
    print(courses)

# Add multiple courses at once (iOS Development and Android Development) with full course details
def test_add_multiple_courses(courses):
    new_courses = {
        'Course_ID': ['CS156', 'CS157'],
        'Course_Name': ['iOS Development', 'Android Development'],
        'Department': ['Web Development', 'Web Development'],
        'Credits': [2, 3],
        'Instructor': ['Dr. Enosh Tsur', 'Prof. Matanel Vatkin'],
        'Difficulty_Level': ['Intermediate', 'Beginner']
    }
    new_course_df = pd.DataFrame(new_courses)
    courses = pd.concat([courses, new_course_df], ignore_index=True)
    print(courses)

# Create a derived column "Course_Level" based on Difficulty_Level with simplified categories (Basic/Advanced)
def test_add_column_course_level(courses):
    courses_copy = courses.copy()
    courses_copy['Course_Level'] = courses_copy['Difficulty_Level'].apply(lambda level: 'Basic' if level == 'Beginner' else 'Advanced')
    print(courses_copy.iloc[:, [1, -1]])

# Create a column categorizing departments as "Technical" or "Theory" based on department name
def test_add_column_department_category(courses):
    theory_categories = ['Data Science', 'Computer Science']
    courses_copy = courses.copy()
    courses_copy['Department_Category'] = courses_copy['Department'].apply(lambda category: 'Theory' if category in theory_categories else 'Technical')
    print(courses_copy.iloc[:, [1, -1]])

# Create course codes by combining Department and Course_ID (e.g., "CS-CS101")
def test_create_course_code(courses):
    courses['Course_ID'] = courses.apply(
        lambda row: f"{reduce(lambda acc, word: acc + word[0], row['Department'].split(), '')}-{row['Course_ID']}",
        axis=1
    )
    print(courses)

# 6. Find all courses taught by instructors whose names start with "Dr."
def test_startswith(courses):
    all_DRs = courses[courses['Instructor'].str.startswith('Dr')]
    print(all_DRs)

# 7. Find all courses in Computer Science and Web Development departments
def test_find_by_department(courses):
    departments = ['Computer Science', 'Web Development']
    print(courses[courses['Department'].isin(departments)])

# 8. Perform a complex query to find all advanced courses with 4 credits taught by specific professors
def test_complex_query(courses):
    professors = ['Dr. Tomer Sagi']
    print(
        courses[
            courses['Credits'] == 4 & courses['Instructor'].isin(professors)
        ]
    )

# 9. Calculate average credits by department
def test_average_credits_by_department(courses):
    print(courses[courses['Department'] == 'Computer Science']['Credits'].mean())

# 10. Find courses with duplicate difficulty levels
def test_duplicate_diff_lvl(courses):
    print(courses[courses.duplicated(subset='Difficulty_Level', keep=False)])

# 11. Increase credits by 1 for all beginner-level courses
def test_increase_credit(courses):
    courses_copy = courses.copy()
    courses_copy.loc[courses_copy['Difficulty_Level'] == 'Beginner', 'Credits'] += 1
    print(courses_copy)

# 12. Update department name 'Web Development' to 'Web Technologies'
def test_web_tech(courses):
    courses_copy = courses.copy()
    courses_copy.loc[courses_copy['Department'] == 'Web Development', 'Department'] = 'Web Technologies'
    print(courses_copy['Department'])

# 13. Add "+1" to all 4-credit courses in Course_ID
def test_adjust_id_column_accordingly(courses):
    courses_copy = courses.copy()
    courses_copy.loc[courses_copy['Credits'] == 4, 'Course_ID'] = courses_copy['Course_ID'].astype(str) + '+1'
    print(courses_copy[['Course_ID', 'Credits']])

# 14. Mark all Computer Science courses as "Core" and others as "Elective" in a new column
def test_update_new_column(courses):
    courses_copy = courses.copy()
    courses_copy['Course_Type'] = courses_copy['Department'].apply(lambda dept: 'Core' if dept == 'Computer Science' else 'Elective')
    print(courses_copy[['Course_ID', 'Course_Name', 'Department', 'Course_Type']])

# 15. Update instructor titles (e.g., change "Dr." to "Professor")
def test_update_title(courses):
    copy_courses = courses.copy()
    copy_courses['Instructor'] = copy_courses['Instructor'].str.replace('Dr.', 'Prof.')
    print(copy_courses['Instructor'])

# 16. Get the first three courses' names and credits using integer-based indexing
def test_iloc(courses):
    print(courses.iloc[:3, [1, 3]])

# 17. Select specific courses using label-based indexing based on Course_ID
def test_loc(courses):
    selected_course_ids = ['CS101', 'WD101']
    print(courses.loc[courses['Course_ID'].isin(selected_course_ids)])

# 18. Extract department and instructor details for a range of courses
def test_department_instructor(courses):
    print(courses.loc[:3, ['Department', 'Instructor']])

# 19. Get all course details for specific Course_IDs using label-based access
def test_course_details(courses):
    course_ids = ['CS101', 'WEB101', 'DS101']
    print(courses.loc[courses['Course_ID'].isin(course_ids), :])

# 20. Select alternate courses (every second course) with their complete details
def test_alternate_courses(courses):
    print(courses.iloc[::2, :])

# 21. Calculate minimum, maximum, and average credits for each department
def test_calculate_minimum(courses):
    min_credits = courses['Credits'].min()
    max_credits = courses['Credits'].max()
    avg_credits = courses['Credits'].mean()
    print(min_credits, max_credits, avg_credits)

# 22. Find the department with the highest average credits
def test_highest_avg_credits(courses):
    avg_credits_by_dept = courses.groupby('Department')['Credits'].mean()
    highest_avg_department = avg_credits_by_dept.idxmax()
    highest_avg_credits = avg_credits_by_dept.max()
    print(f"Department with the highest average credits: {highest_avg_department} ({highest_avg_credits:.2f} credits)")


# 23. Group courses by difficulty level and count instructors
def test_group_by_difficulty_instructors(courses):
    print(courses.groupby('Difficulty_Level')['Instructor'].nunique())

# 24. Calculate the distribution of credits within each department
def test_calculate_credits_distribution(courses):
    print(courses.groupby('Department')['Credits'].describe())

# 25. Find departments with the most and least number of courses
def test_num_of_courses_for_departments(courses):
    courses_count_by_dept = courses.groupby('Department').size()

    max_courses_department = courses_count_by_dept.idxmax()
    min_courses_department = courses_count_by_dept.idxmin()
    max_courses_count = courses_count_by_dept.max()
    min_courses_count = courses_count_by_dept.min()

    print(f"Department with the most courses: {max_courses_department} ({max_courses_count} courses)")
    print(f"Department with the least courses: {min_courses_department} ({min_courses_count} courses)")
