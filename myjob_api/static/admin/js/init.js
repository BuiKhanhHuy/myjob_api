// All the settings are stored in the window.settings object
const SETTINGS = window.settings;
// Firebase configuration
const FIREBASE_CONFIG = SETTINGS.firebase;
// API endpoints
const ENDPOINTS = {
    "STATISTICAL_APPLICATION_CHART": "/admin/api/application-chart/",
    "STATISTICAL_USER_CHART": "/admin/api/user-chart/",
    "STATISTICAL_CAREER_CHART": "/admin/api/career-chart/",
    "STATISTICAL_JOB_POST_CHART": "/admin/api/job-post-chart/",
}
// Default page size
const PAGE_SIZE_DEFAULT = 10;

export { FIREBASE_CONFIG, ENDPOINTS, PAGE_SIZE_DEFAULT };