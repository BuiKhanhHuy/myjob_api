# Environment: Development
ENV_DEV = "development"
ENV_PROD = "production"

# Refix for all routes
ROUTES_PREFIX = "api/"
COMMON_PREFIX = "common/"
AUTHENTICATION_PREFIX = "auth/"
INFO_PREFIX = "info/"
JOB_PREFIX = "job/"
MYJOB_PREFIX = "myjob/"

MIDDLEWARE_ALLOW_ANY_FOR_ROUTES = [
    "/" + ROUTES_PREFIX + COMMON_PREFIX + "configs/",
    "/" + ROUTES_PREFIX + COMMON_PREFIX + "districts/",
    "/" + ROUTES_PREFIX + COMMON_PREFIX + "top-careers/",
    "/" + ROUTES_PREFIX + COMMON_PREFIX + "all-careers/",

    "/" + ROUTES_PREFIX + AUTHENTICATION_PREFIX + "token/",
    "/" + ROUTES_PREFIX + AUTHENTICATION_PREFIX + "convert-token/",
    "/" + ROUTES_PREFIX + AUTHENTICATION_PREFIX + "revoke-token/",
    "/" + ROUTES_PREFIX + AUTHENTICATION_PREFIX + "email-exists/",
    "/" + ROUTES_PREFIX + AUTHENTICATION_PREFIX + "check-creds/",
]
