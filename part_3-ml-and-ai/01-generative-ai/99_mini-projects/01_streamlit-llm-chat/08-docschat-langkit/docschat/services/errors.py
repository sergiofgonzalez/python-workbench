"""Custom Application Errors"""


class PromptSecurityRiskError(Exception):
    pass


class ResponseSecurityRiskError(Exception):
    pass


class ResponseRelevanceError(Exception):
    pass
