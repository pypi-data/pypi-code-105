from django.contrib import admin

from ob_dj_survey.core.survey.models import (
    Survey,
    SurveyAnswer,
    SurveyChoice,
    SurveyQuestion,
    SurveyResponse,
    SurveySection,
)


class SurveyQuestionInlineAdmin(admin.TabularInline):
    model = SurveyQuestion
    extra = 0


class SurveySectionInlineAdmin(admin.TabularInline):
    model = SurveySection
    extra = 0


class SurveyInlineAdmin(admin.TabularInline):
    model = Survey
    extra = 0


class SurveyChoiceInlineAdmin(admin.TabularInline):
    model = SurveyChoice
    extra = 0


class SurveyResponseInlineAdmin(admin.TabularInline):
    model = SurveyResponse
    extra = 0


class SurveyAnswersInlineAdmin(admin.TabularInline):
    model = SurveyAnswer
    extra = 0


class SurveyResponsesAnswersInline(admin.TabularInline):
    model = SurveyAnswer.responses.through


@admin.register(SurveySection)
class SurveySectionAdmin(admin.ModelAdmin,):
    list_display = ["name", "description", "meta", "created_at"]
    fieldsets = ((None, {"fields": ("name", "description", "meta")},),)
    list_editable = ["description"]
    inlines = [SurveyQuestionInlineAdmin]


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin,):
    fieldsets = ((None, {"fields": ("name", "meta",)},),)
    list_display = ["name", "meta", "created_at"]
    inlines = [SurveyAnswersInlineAdmin, SurveyQuestionInlineAdmin]


@admin.register(SurveyChoice)
class SurveyChoiceAdmin(admin.ModelAdmin,):
    fieldsets = ((None, {"fields": ("title", "question", "description", "meta",)},),)
    list_display = ["title", "question", "description", "meta", "created_at"]
    list_editable = ["question", "description"]
    inlines = [SurveyResponseInlineAdmin]


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin,):
    fieldsets = (
        (
            None,
            {"fields": ("title", "type", "survey", "section", "is_active", "meta",)},
        ),
    )
    list_display = ["title", "type", "is_active", "section", "meta", "created_at"]
    inlines = [SurveyChoiceInlineAdmin, SurveyResponseInlineAdmin]


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin,):
    list_display = ["question", "choice", "value", "meta", "updated_at", "created_at"]
    list_display_links = ["question"]
    fieldsets = ((None, {"fields": ("question", "choice", "value", "meta",)},),)
    list_editable = ["choice", "value"]


@admin.register(SurveyAnswer)
class SurveyAnswersAdmin(admin.ModelAdmin,):
    list_display = ["status", "updated_at", "meta", "created_at"]
    fieldsets = (
        (None, {"fields": ("survey", "responses", "created_by", "status", "meta",)},),
    )
    inlines = [
        SurveyResponsesAnswersInline,
    ]
