from utils.caching import load_cache


class AppState:
    def __init__(self):
        self.current_view_title = "Dashboard"
        # cache
        self.cache = load_cache()
        # project folder
        self.project_folder = None
        # AI
        self.ai_assistant = "Gemini"
        # upload view
        self.vuln_type_map = {}
        self.vuln_type_uuid = ""
        self.vuln_type_context_uuid = ""
        self.current_finding_index = 0
        self.current_image_index = 0
        self.findings = []
        self.metadata = None
        self.ai_suggestions = []
        self.ai_suggestions_editable = []
        self.org_uuid = ""
        self.org_name = ""
        self.asset_uuid = ""
        self.asset_name = ""
        self.test_uuid = ""
        self.test_id = ""
        self.uploaded_vulns = {}
        self.folder_stack = []
        self.current_items = []
        self.cvss_data = []
        self.fetched_migration_vulns = None
        self.app_version = "0.4b"
