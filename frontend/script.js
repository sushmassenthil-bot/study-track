const API_BASE = "http://127.0.0.1:8000";


// ======================================================
// API HELPER
// ======================================================

async function apiRequest(url, options = {}) {
    const response = await fetch(`${API_BASE}${url}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    });

    if (!response.ok) {
        let errorMessage = "Something went wrong.";

        try {
            const errorData = await response.json();
            errorMessage = errorData.detail || errorMessage;
        } catch {
            // Keep default error message
        }

        throw new Error(errorMessage);
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}


// ======================================================
// NOTIFICATIONS
// ======================================================

function showNotification(message, type = "success") {
    const notification = document.getElementById("notification");
    const messageElement =
        document.getElementById("notification-message");

    if (!notification || !messageElement) return;

    messageElement.textContent = message;

    notification.className = `notification ${type}`;

    setTimeout(() => {
        notification.classList.add("hidden");
    }, 3000);
}


// ======================================================
// NAVIGATION
// ======================================================

function setupNavigation() {
    const navItems = document.querySelectorAll(".nav-item");
    const sections = document.querySelectorAll(".page-section");
    const pageTitle = document.getElementById("page-title");

    navItems.forEach(button => {
        button.addEventListener("click", () => {
            const targetSection = button.dataset.section;

            navItems.forEach(item => {
                item.classList.remove("active");
            });

            button.classList.add("active");

            sections.forEach(section => {
                section.classList.remove("active");
            });

            const target = document.getElementById(targetSection);

            if (target) {
                target.classList.add("active");
            }

            if (pageTitle) {
                const titles = {
                    dashboard: "Dashboard",
                    students: "Students",
                    courses: "Courses",
                    algorithms: "Search & Algorithms",
                    advisor: "AI Study Advisor"
                };

                pageTitle.textContent =
                    titles[targetSection] || "Dashboard";
            }
        });
    });

    // Buttons such as "View All"
    document.querySelectorAll("[data-section-target]").forEach(button => {
        button.addEventListener("click", () => {
            const targetSection = button.dataset.sectionTarget;

            const navButton =
                document.querySelector(
                    `.nav-item[data-section="${targetSection}"]`
                );

            if (navButton) {
                navButton.click();
            }
        });
    });
}


// ======================================================
// STUDENTS
// ======================================================

async function loadStudents(minAge = null) {
    try {
        let url = "/students/";

        if (minAge) {
            url += `?min_age=${encodeURIComponent(minAge)}`;
        }

        const students = await apiRequest(url);

        const table = document.getElementById("students-table");
        const dashboardTable =
            document.getElementById("dashboard-students");

        // Main student table
        if (table) {
            table.innerHTML = "";

            if (students.length === 0) {
                table.innerHTML = `
                    <tr>
                        <td colspan="5" class="empty-state">
                            No students found.
                        </td>
                    </tr>
                `;
            } else {
                students.forEach(student => {
                    const row = document.createElement("tr");

                    row.innerHTML = `
                        <td>${student.id}</td>
                        <td>${escapeHtml(student.name)}</td>
                        <td>${escapeHtml(student.email)}</td>
                        <td>${student.age}</td>
                        <td>
                            <button
                                class="danger-button"
                                onclick="deleteStudent(${student.id})">
                                Delete
                            </button>
                        </td>
                    `;

                    table.appendChild(row);
                });
            }
        }

        // Dashboard student table
        if (dashboardTable) {
            dashboardTable.innerHTML = "";

            const recentStudents = students.slice(0, 5);

            if (recentStudents.length === 0) {
                dashboardTable.innerHTML = `
                    <tr>
                        <td colspan="3" class="empty-state">
                            No students found.
                        </td>
                    </tr>
                `;
            } else {
                recentStudents.forEach(student => {
                    const row = document.createElement("tr");

                    row.innerHTML = `
                        <td>${escapeHtml(student.name)}</td>
                        <td>${escapeHtml(student.email)}</td>
                        <td>${student.age}</td>
                    `;

                    dashboardTable.appendChild(row);
                });
            }
        }

        // Dashboard statistics
        const totalStudents =
            document.getElementById("total-students");

        if (totalStudents) {
            totalStudents.textContent = students.length;
        }

        const studentsOverAge =
            document.getElementById("students-over-age");

        if (studentsOverAge) {
            studentsOverAge.textContent =
                students.filter(student => student.age >= 21).length;
        }

        return students;

    } catch (error) {
        console.error("Error loading students:", error);

        showNotification(
            `Unable to load students: ${error.message}`,
            "error"
        );
    }
}


async function createStudent(event) {
    event.preventDefault();

    const name =
        document.getElementById("student-name")?.value.trim();

    const email =
        document.getElementById("student-email")?.value.trim();

    const age =
        Number(document.getElementById("student-age")?.value);

    if (!name || !email || !age) {
        showNotification(
            "Please fill in all student fields.",
            "error"
        );
        return;
    }

    try {
        await apiRequest("/students/", {
            method: "POST",
            body: JSON.stringify({
                name,
                email,
                age
            })
        });

        showNotification("Student added successfully.");

        document.getElementById("student-form").reset();

        hideStudentForm();

        await loadStudents();

        await loadStudentReport();

    } catch (error) {
        showNotification(error.message, "error");
    }
}


async function deleteStudent(studentId) {
    const confirmed = confirm(
        "Are you sure you want to delete this student?"
    );

    if (!confirmed) return;

    try {
        await apiRequest(`/students/${studentId}`, {
            method: "DELETE"
        });

        showNotification("Student deleted successfully.");

        await loadStudents();
        await loadCourses();
        await loadStudentReport();

    } catch (error) {
        showNotification(error.message, "error");
    }
}


// ======================================================
// STUDENT FORM
// ======================================================

function showStudentForm() {
    const container =
        document.getElementById("student-form-container");

    if (container) {
        container.classList.remove("hidden");
    }
}


function hideStudentForm() {
    const container =
        document.getElementById("student-form-container");

    if (container) {
        container.classList.add("hidden");
    }
}


// ======================================================
// STUDENT FILTER
// ======================================================

async function applyAgeFilter() {
    const input =
        document.getElementById("min-age-filter");

    const value = input?.value.trim();

    if (!value) {
        await loadStudents();
        return;
    }

    const minAge = Number(value);

    if (!minAge || minAge < 1) {
        showNotification(
            "Please enter a valid minimum age.",
            "error"
        );
        return;
    }

    await loadStudents(minAge);
}


// ======================================================
// STUDENT REPORT
// ======================================================

async function loadStudentReport() {
    try {
        const result = await apiRequest(
            "/students/report?min_age=21"
        );

        const reportContainer =
            document.getElementById("dashboard-report");

        if (!reportContainer) return;

        reportContainer.innerHTML = `
            <pre>${escapeHtml(result.report)}</pre>

            <p style="margin-top: 15px;">
                <strong>
                    Students aged 21+:
                </strong>
                ${result.count_meeting_min_age}
            </p>
        `;

    } catch (error) {
        console.error(
            "Error loading student report:",
            error
        );
    }
}


// ======================================================
// COURSES
// ======================================================

async function loadCourses() {
    try {
        const courses = await apiRequest("/courses/");

        const table =
            document.getElementById("courses-table");

        const totalCourses =
            document.getElementById("total-courses");

        if (totalCourses) {
            totalCourses.textContent = courses.length;
        }

        if (!table) return;

        table.innerHTML = "";

        if (courses.length === 0) {
            table.innerHTML = `
                <tr>
                    <td colspan="5" class="empty-state">
                        No courses found.
                    </td>
                </tr>
            `;

            return;
        }

        courses.forEach(course => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${course.id}</td>
                <td>${escapeHtml(course.course_name)}</td>
                <td>${course.credits}</td>
                <td>${course.student_id}</td>
                <td>
                    <button
                        class="danger-button"
                        onclick="deleteCourse(${course.id})">
                        Delete
                    </button>
                </td>
            `;

            table.appendChild(row);
        });

    } catch (error) {
        console.error("Error loading courses:", error);

        showNotification(
            `Unable to load courses: ${error.message}`,
            "error"
        );
    }
}


async function createCourse(event) {
    event.preventDefault();

    const courseName =
        document.getElementById("course-name")?.value.trim();

    const credits =
        Number(
            document.getElementById("course-credits")?.value
        );

    const studentId =
        Number(
            document.getElementById("course-student")?.value
        );

    if (!courseName || !credits || !studentId) {
        showNotification(
            "Please fill in all course fields.",
            "error"
        );
        return;
    }

    try {
        await apiRequest("/courses/", {
            method: "POST",
            body: JSON.stringify({
                course_name: courseName,
                credits,
                student_id: studentId
            })
        });

        showNotification("Course added successfully.");

        document.getElementById("course-form").reset();

        hideCourseForm();

        await loadCourses();

    } catch (error) {
        showNotification(error.message, "error");
    }
}


async function deleteCourse(courseId) {
    const confirmed = confirm(
        "Are you sure you want to delete this course?"
    );

    if (!confirmed) return;

    try {
        await apiRequest(`/courses/${courseId}`, {
            method: "DELETE"
        });

        showNotification("Course deleted successfully.");

        await loadCourses();

    } catch (error) {
        showNotification(error.message, "error");
    }
}


// ======================================================
// COURSE FORM
// ======================================================

function showCourseForm() {
    const container =
        document.getElementById("course-form-container");

    if (container) {
        container.classList.remove("hidden");
    }
}


function hideCourseForm() {
    const container =
        document.getElementById("course-form-container");

    if (container) {
        container.classList.add("hidden");
    }
}


// ======================================================
// ALGORITHMS
// ======================================================

async function loadRoster() {
    const resultContainer =
        document.getElementById("roster-result");

    if (!resultContainer) return;

    resultContainer.innerHTML =
        `<p class="loading">Sorting students...</p>`;

    try {
        const students =
            await apiRequest("/algorithms/roster");

        if (!students.length) {
            resultContainer.innerHTML =
                `<p>No students available.</p>`;
            return;
        }

        resultContainer.innerHTML = students
            .map((student, index) => `
                <div style="padding: 8px 0;">
                    <strong>${index + 1}.</strong>
                    ${escapeHtml(student.name)}
                    — ${student.age} years
                </div>
            `)
            .join("");

    } catch (error) {
        resultContainer.innerHTML =
            `<p>${escapeHtml(error.message)}</p>`;
    }
}


async function searchStudent(event) {
    event.preventDefault();

    const name =
        document.getElementById("search-name")?.value.trim();

    const resultContainer =
        document.getElementById("search-result");

    if (!name) {
        showNotification(
            "Enter a student name.",
            "error"
        );
        return;
    }

    if (!resultContainer) return;

    resultContainer.innerHTML =
        `<p class="loading">Searching...</p>`;

    try {
        const result = await apiRequest(
            `/algorithms/search?name=${encodeURIComponent(name)}`
        );

        resultContainer.innerHTML = `
            <h3>Student Found</h3>

            <p>
                <strong>Name:</strong>
                ${escapeHtml(result.student.name)}
            </p>

            <p>
                <strong>Email:</strong>
                ${escapeHtml(result.student.email)}
            </p>

            <p>
                <strong>Age:</strong>
                ${result.student.age}
            </p>

            <p>
                <strong>Index:</strong>
                ${result.index}
            </p>
        `;

    } catch (error) {
        resultContainer.innerHTML = `
            <p>${escapeHtml(error.message)}</p>
        `;
    }
}


// ======================================================
// AI STUDY ADVISOR
// ======================================================

async function getStudyAdvice(event) {
    event.preventDefault();

    const prompt =
        document.getElementById("ai-prompt")?.value.trim();

    const resultContainer =
        document.getElementById("ai-result");

    const adviceContainer =
        document.getElementById("ai-advice");

    const submitButton =
        document.getElementById("ai-submit");

    if (!prompt) {
        showNotification(
            "Please enter a study question.",
            "error"
        );
        return;
    }

    if (resultContainer) {
        resultContainer.classList.remove("hidden");
    }

    if (adviceContainer) {
        adviceContainer.textContent =
            "Generating advice...";
    }

    if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = "Generating...";
    }

    try {
        const result = await apiRequest(
            "/ai/study-advice",
            {
                method: "POST",
                body: JSON.stringify({
                    prompt
                })
            }
        );

        if (adviceContainer) {
            adviceContainer.textContent =
                result.advice;
        }

    } catch (error) {
        if (adviceContainer) {
            adviceContainer.textContent =
                `Unable to generate advice: ${error.message}`;
        }
    } finally {
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent =
                "Get Study Advice";
        }
    }
}


// ======================================================
// HTML ESCAPING
// ======================================================

function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
}


// ======================================================
// INITIALIZATION
// ======================================================

document.addEventListener("DOMContentLoaded", () => {

    setupNavigation();

    // Student form
    document
        .getElementById("student-form")
        ?.addEventListener(
            "submit",
            createStudent
        );

    document
        .getElementById("open-student-form")
        ?.addEventListener(
            "click",
            showStudentForm
        );

    document
        .getElementById("close-student-form")
        ?.addEventListener(
            "click",
            hideStudentForm
        );

    document
        .getElementById("cancel-student-form")
        ?.addEventListener(
            "click",
            hideStudentForm
        );

    // Student filter
    document
        .getElementById("apply-age-filter")
        ?.addEventListener(
            "click",
            applyAgeFilter
        );

    // Course form
    document
        .getElementById("course-form")
        ?.addEventListener(
            "submit",
            createCourse
        );

    document
        .getElementById("open-course-form")
        ?.addEventListener(
            "click",
            showCourseForm
        );

    document
        .getElementById("close-course-form")
        ?.addEventListener(
            "click",
            hideCourseForm
        );

    document
        .getElementById("cancel-course-form")
        ?.addEventListener(
            "click",
            hideCourseForm
        );

    // Algorithms
    document
        .getElementById("load-roster")
        ?.addEventListener(
            "click",
            loadRoster
        );

    document
        .getElementById("search-form")
        ?.addEventListener(
            "submit",
            searchStudent
        );

    // AI
    document
        .getElementById("ai-form")
        ?.addEventListener(
            "submit",
            getStudyAdvice
        );

    // Initial data
    loadStudents();
    loadCourses();
    loadStudentReport();
});