"""Playwright tests for the SRP Cards web interface."""

import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def base_url():
    """Return file:// URL for the web interface."""
    html_path = Path(__file__).resolve().parent.parent / "web" / "index.html"
    return f"file://{html_path}"


@pytest.fixture(autouse=True)
def navigate(page: Page, base_url: str):
    """Navigate to the app before each test."""
    page.goto(base_url)


class TestNavigation:
    def test_page_loads(self, page: Page):
        expect(page.locator("nav")).to_be_visible()
        expect(page.locator("#dashboardBtn")).to_be_visible()

    def test_default_page_is_dashboard(self, page: Page):
        expect(page.locator("#dashboardPage")).to_be_visible()

    def test_navigate_to_all_pages(self, page: Page):
        pages = {
            "onboardingBtn": "onboardingPage",
            "createBtn": "createPage",
            "trackingBtn": "trackingPage",
            "cardOptionsBtn": "cardOptionsPage",
            "helpBtn": "helpPage",
            "offboardingBtn": "offboardingPage",
        }
        for btn_id, page_id in pages.items():
            page.click(f"#{btn_id}")
            expect(page.locator(f"#{page_id}")).to_be_visible()


class TestDashboard:
    def test_bed_grid_renders_30_beds(self, page: Page):
        buttons = page.locator("#bedGrid button")
        expect(buttons).to_have_count(30)

    def test_select_bed_shows_info(self, page: Page):
        page.click("#bedBtn_B1")
        expect(page.locator("#bedNumberInfo")).to_be_visible()
        expect(page.locator("#bedNumberDisplay")).to_have_text("B1")


class TestPrintCards:
    def test_format_selection_visible(self, page: Page):
        page.click("#createBtn")
        expect(page.locator("#formatCards")).to_be_visible()

    def test_quadrant_format_shows_exercises(self, page: Page):
        page.click("#createBtn")
        # Quadrant is default format, grid should exist in DOM
        expect(page.locator("#quadExerciseGrid")).to_be_attached()


class TestTrackingSheet:
    def test_tracking_sheet_renders(self, page: Page):
        page.click("#trackingBtn")
        expect(page.locator("#trackingSheetPreview")).to_be_visible()
        expect(page.locator("#trackingTablesContainer")).to_be_visible()

    def test_tracking_tables_have_content(self, page: Page):
        page.click("#trackingBtn")
        tables = page.locator("#trackingTablesContainer table")
        # 4 exercise categories + 1 comfort level = 5 tables
        expect(tables).to_have_count(5)


class TestCardOptions:
    def test_categories_render(self, page: Page):
        page.click("#cardOptionsBtn")
        container = page.locator("#cardOptionsCategoriesContainer")
        expect(container).to_be_visible()
        # Should have 4 category sections
        expect(container.locator("> div")).to_have_count(4)

    def test_exercise_steps_draggable(self, page: Page):
        page.click("#cardOptionsBtn")
        draggable = page.locator("li[draggable='true']")
        assert draggable.count() > 0

    def test_copy_card_state(self, page: Page):
        page.click("#cardOptionsBtn")
        # Grant clipboard permissions
        page.context.grant_permissions(["clipboard-read", "clipboard-write"])
        page.click("text=Copy Card State")
        expect(page.locator("#copyConfirmation")).to_be_visible()

    def test_add_exercise(self, page: Page):
        page.click("#cardOptionsBtn")
        initial_count = page.locator("#cardOptionsCategoriesContainer ol").count()

        # Intercept dialog to enter exercise name and steps
        page.on("dialog", lambda dialog: dialog.accept(
            "Test Exercise" if "name" in dialog.message.lower() else "Step 1, Step 2"
        ))
        page.locator("text=+ Add Exercise").first.click()


class TestOnboardingGate:
    def test_care_setting_visible(self, page: Page):
        page.click("#onboardingBtn")
        expect(page.locator("#onboardSettingGrid")).to_be_visible()

    def test_tier0_visible(self, page: Page):
        page.click("#onboardingBtn")
        expect(page.locator("#tier0Section")).to_be_visible()

    def test_tier1_locked_initially(self, page: Page):
        page.click("#onboardingBtn")
        tier1 = page.locator("#tier1Section")
        expect(tier1).to_have_css("pointer-events", "none")

    def test_hard_exclusion_gcs(self, page: Page):
        page.click("#onboardingBtn")
        page.select_option("#gateGCS", "10")
        expect(page.locator("#tier0Result")).to_contain_text("EXCLUDE")

    def test_hard_exclusion_mrs(self, page: Page):
        page.click("#onboardingBtn")
        page.select_option("#gatemRS", "5")
        expect(page.locator("#tier0Result")).to_contain_text("EXCLUDE")

    def test_hard_exclusion_nihss9(self, page: Page):
        page.click("#onboardingBtn")
        page.select_option("#gateNIHSS9", "3")
        expect(page.locator("#tier0Result")).to_contain_text("EXCLUDE")

    def test_proceed_clean_unlocks_tier1(self, page: Page):
        page.click("#onboardingBtn")
        page.select_option("#gateGCS", "15")
        tier1 = page.locator("#tier1Section")
        expect(tier1).to_have_css("pointer-events", "auto")

    def test_fast_comprehension_fail_defers(self, page: Page):
        page.click("#onboardingBtn")
        page.select_option("#gateGCS", "15")
        page.select_option("#gateFASTComp", "fail")
        expect(page.locator("#tier1Result")).to_contain_text("DEFER")

    def test_fast_pass_unlocks_tier2(self, page: Page):
        page.click("#onboardingBtn")
        page.select_option("#gateGCS", "15")
        page.select_option("#gateFASTComp", "pass")
        page.select_option("#gateFASTExpr", "pass")
        tier2 = page.locator("#tier2Section")
        expect(tier2).to_have_css("pointer-events", "auto")

    def test_moca_routing_full(self, page: Page):
        page.click("#onboardingBtn")
        page.select_option("#gateGCS", "15")
        page.select_option("#gateFASTComp", "pass")
        page.select_option("#gateFASTExpr", "pass")
        page.select_option("#gateMoCA", "28")
        expect(page.locator("#tier2Result")).to_contain_text("Full card set")

    def test_moca_routing_simplified(self, page: Page):
        page.click("#onboardingBtn")
        page.select_option("#gateGCS", "15")
        page.select_option("#gateFASTComp", "pass")
        page.select_option("#gateFASTExpr", "pass")
        page.select_option("#gateMoCA", "20")
        expect(page.locator("#tier2Result")).to_contain_text("Simplified")

    def test_moca_routing_defer(self, page: Page):
        page.click("#onboardingBtn")
        page.select_option("#gateGCS", "15")
        page.select_option("#gateFASTComp", "pass")
        page.select_option("#gateFASTExpr", "pass")
        page.select_option("#gateMoCA", "10")
        expect(page.locator("#tier2Result")).to_contain_text("DEFER")

    def test_acute_setting_flags_only(self, page: Page):
        page.click("#onboardingBtn")
        page.click("input[name='careSetting'][value='acute']")
        expect(page.locator("#acuteNotice")).to_be_visible()

    def test_reset_clears_all(self, page: Page):
        page.click("#onboardingBtn")
        page.select_option("#gateGCS", "15")
        page.click("text=Reset All")
        expect(page.locator("#gateGCS")).to_have_value("")


class TestOffboarding:
    def test_offboarding_page_loads(self, page: Page):
        page.click("#offboardingBtn")
        expect(page.locator("text=Evaluation Priority")).to_be_visible()

    def test_card_inputs_render(self, page: Page):
        page.click("#offboardingBtn")
        inputs = page.locator("#offCardInputs > div")
        # 4 categories x 3 exercises = 12 cards
        expect(inputs).to_have_count(12)

    def test_session_gap_triggers(self, page: Page):
        page.click("#offboardingBtn")
        page.fill("#offDaysSinceSession", "20")
        page.fill("#offR_hand_0_2", "0.9")
        page.locator("#offboardingPage button", has_text="Evaluate Offboarding Triggers").click()
        expect(page.locator("#offResultState")).to_contain_text("SESSION GAP")

    def test_withdrawal_flow(self, page: Page):
        page.click("#offboardingBtn")
        page.on("dialog", lambda dialog: dialog.accept())
        page.locator("#offboardingPage button", has_text="Withdraw").click()
        expect(page.locator("#offResultState")).to_contain_text("WITHDRAWN")

    def test_reset_clears_offboarding(self, page: Page):
        page.click("#offboardingBtn")
        page.fill("#offDaysSinceSession", "20")
        page.on("dialog", lambda dialog: dialog.accept())
        page.locator("#offboardingPage button", has_text="Reset").click()
        expect(page.locator("#offResultSection")).to_be_hidden()


class TestMobileResponsive:
    def test_hamburger_menu_visible_on_mobile(self, page: Page):
        page.set_viewport_size({"width": 375, "height": 812})
        page.reload()
        expect(page.locator("#mobileMenuBtn")).to_be_visible()

    def test_nav_hidden_on_mobile(self, page: Page):
        page.set_viewport_size({"width": 375, "height": 812})
        page.reload()
        expect(page.locator("#navLinks")).to_be_hidden()

    def test_hamburger_opens_nav(self, page: Page):
        page.set_viewport_size({"width": 375, "height": 812})
        page.reload()
        page.click("#mobileMenuBtn")
        expect(page.locator("#navLinks")).to_be_visible()

    def test_nav_closes_after_selection(self, page: Page):
        page.set_viewport_size({"width": 375, "height": 812})
        page.reload()
        page.click("#mobileMenuBtn")
        page.click("#helpBtn")
        expect(page.locator("#navLinks")).to_be_hidden()
