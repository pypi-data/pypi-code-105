# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['allianceutils',
 'allianceutils.api',
 'allianceutils.auth',
 'allianceutils.management',
 'allianceutils.management.commands',
 'allianceutils.middleware',
 'allianceutils.serializers',
 'allianceutils.templatetags',
 'allianceutils.util',
 'allianceutils.views']

package_data = \
{'': ['*'], 'allianceutils': ['bin/*']}

install_requires = \
['Django>=2.2', 'isort>=4']

setup_kwargs = {
    'name': 'django-allianceutils',
    'version': '2.1.0',
    'description': 'Alliance Software common utilities for Django',
    'long_description': '# Alliance Utils\n\n![CI Tests](https://github.com/AllianceSoftware/django-allianceutils/workflows/Django%20CI/badge.svg)\n\nA collection of utilities for django projects from [Alliance Software](https://www.alliancesoftware.com.au/).\n\n* [Installation](#installation)\n* [Usage](#usage)\n    * [API](#api)\n    * [Auth](#auth)\n    * [Decorators](#decorators)\n    * [Filters](#filters)\n    * [Management](#management)\n        * [Commands](#commands)\n        * [Checks](#checks)\n    * [Middleware](#middleware)\n    * [Migrations](#migrations)\n    * [Models](#models)\n    * [Rules](#rules)\n    * [Serializers](#serializers)\n    * [Template Tags](#template-tags)\n    * [Util](#util)\n* [Changelog](#changelog)\n\n## Installation\n\n`pip install django-allianceutils`\n\n## System Requirements\n\n* Tested with django 2.2 and 3.2\n  * Pull requests accepted for other versions, but at minimum we test against current LTS versions\n* Python >=3.6 (no python 3.5 support)\n\n## Usage\n\n### API\n\n#### Mixins\n\n##### SerializerOptInFieldsMixin\n\nRegulates fields exposed on a Serializer by default & as requested based on query parameters or context.\n\n* Pass \'include_fields\' / \'opt_in_fields\' thru query params or context to use.\n* multiple fields can either be separated by comma\n  eg, `/?include_fields=first_name,email&opt_in_fields=gait_recognition_prediction`\n* or passed in the traditional list fashion\n  eg, `/?include_fields=first_name&include_fields=email&opt_in_fields=gait_recognition_prediction`\n* or mixed eg, `/?include_fields=first_name,email&include_fields=boo`\n* By default, all "fields" defined in serializer, minus those listed in "opt_in_fields" would be returned.\n* If "include_fields" is supplied, only fields requested this way would be returned.\n* If "opt_in_fields" is supplied, fields requested this way PLUS fields from #1 or #2 would be returned.\n* Pinned fields are always returned (defaults to primary key)\n\nUsage:\n\n```python\nclass UserSerializer(SerializerOptInFieldsMixin, ModelSerializer):\n    class Meta:\n        model = User\n        fields = (\n            "id",\n            "first_name",\n            "last_name",\n            "email",\n            "region",\n            "activated_at",\n            "is_staff",\n        )\n        # These fields only returned if explicitly requested\n        opt_in_only_fields = ["activated_at", "is_staff"]\n```\n\n#### Permissions\n\n##### register_custom_permissions\n\n* Creates permissions that have no model by linking them to an empty content type\n* Django creates permissions as part of\n  the [`post_migrate` signal](https://docs.djangoproject.com/en/stable/ref/signals/#post-migrate)\n\nUsage\n\n```py\ndef on_post_migrate(sender, **kwargs):\n    register_custom_permissions("myapp", ("my_perm", "My Permission"))\n```\n\n##### SimpleDjangoObjectPermissions\n\nPermission class for Django Rest Framework that adds support for object level permissions.\n\nDiffers from just DRF\'s [DjangoObjectPermissions](https://www.django-rest-framework.org/api-guide/permissions/#object-level-permissions) because it\n* does not require a queryset\n* uses the same permission for every request http method and ViewSet method \n\nNotes\n* The default django permissions system will [always return False](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#handling-object-permissions) if given an object; you must be using another permissions backend\n* As per [DRF documentation](http://www.django-rest-framework.org/api-guide/permissions/#object-level-permissions): get_object() is only required if you want to implement object-level permissions\n* **WARNING** If you override `get_object()` then you need to *manually* invoke `self.check_object_permissions(self.request, obj)`\n* Will attempt to check permission both globally and on a per-object basis but considers it an error if the check returns True for both\n*   \n\nUsage\n* See [DRF permissions policy](https://www.django-rest-framework.org/api-guide/permissions/#setting-the-permission-policy) for details on apply Permissions policies globally\n\n* To apply to a specific view you need to set `permission_required`\n```python\nclass MyAPIView(SimpleDjangoObjectPermissions, APIView):\n        permission_required = \'my_module.my_permission\'\n        permission_classes = [allianceutils.api.permissions.SimpleDjangoObjectPermissions] \n```\n\nIf you have no object level permissions (eg. from rules) then it will just do a static permission check.\n\n##### GenericDjangoViewsetPermissions\n\n* Map viewset actions to Django permissions.\n  * The model used for permission is extracted from the ViewSet\n    * If you implement `get_permission_model` on the ViewSet that will be used\n    * Otherwise it will call `get_queryset` on the ViewSet and extract the model from the returned queryset \n * To alter this behaviour extends `GenericDjangoViewsetPermissions` and implement `get_model` \n* Usage example:\n```\nclass MyViewSet(GenericDjangoViewsetPermissions, viewsets.ModelViewSet):\n    queryset = MyModel.objects.all()\n    serializer_class = MySerializer\n```\n* `GenericDjangoViewsetPermissions.default_actions_to_perms_map` defines the default set of permissions. These can be extended or overridden using `actions_to_perms_map`:\n```\nclass MyViewSet(GenericDjangoViewsetPermissions, viewsets.ModelViewSet):\n\n    # ...\n\n    actions_to_perms_map = {\n        \'create\': []\n    }\n```\n* No permissions will be required for the create action, but permissions for other actions will remain unchanged.\n* By default permissions checks are passed the relevant model instance for per-object permission checks\n    * This assumes that your backend doesn\'t ignore the model object (default django permissions simply ignore any object passed to a permissions check)\n    * Since there is no model object, functions decorated with `@list_route` will pass `None` as the permissions check object\n\n#### Parsers\n\n##### CamelCaseJSONParser\n\nParser that recursively turns camelcase keys into underscored keys for JSON data.\nThis can be set globally on the [DEFAULT_PARSER_CLASSES](https://www.django-rest-framework.org/api-guide/settings/#default_parser_classes)\nsetting or on a ViewSet on the `parser_classes` property.\n\n##### CamelCaseMultiPartJSONParser\n\nParser that recursively turns camelcase keys into underscored keys for JSON data and handles file uploads.\nThis parser supports receiving JSON data where a field value anywhere in the structure can be a file.\nThis is achieved on the frontend by converting a structure like:\n\n```js\n{\n    name: \'Test\',\n    photo: File,\n}\n```\n\nAnd converting it to\n\n```js\n{\n    name: \'Test\',\n    photo: \'____ATTACHED_FILE_ID_1\',\n}\n```\n\nThis is then set on a field `jsonData` and the file is set on `____ATTACHED_FILE_ID_1` and submitted\nas multipart.\nThis parser then handles parsing the JSON data into a dict and setting each attached file on the\ncorrect key in the dict.\nNote that this works with nested data (ie. any File anywhere in a nested JSON structure is supported).\nTo activate this behaviour the `X-MultiPart-JSON` header must be set to \'1\' or \'true\'. If this header\nis not set it falls back to the default behaviour of MultiPartParser\nThis can be set globally on the [DEFAULT_PARSER_CLASSES](https://www.django-rest-framework.org/api-guide/settings/#default_parser_classes)\nsetting or on a ViewSet on the `parser_classes` property.\nExample frontend code to activate:\n```js\nlet fileCount = 0;\nconst files = {};\nconst replacer = (key, value) => {\n    if (value instanceof File) {\n        const id = `____ATTACHED_FILE_ID_${fileCount++}`;\n        files[id] = value;\n        return id;\n    }\n    return value;\n};\nconst stringifiedData = JSON.stringify(data, replacer);\nconst body = new FormData();\nconst body.append(\'jsonData\', stringifiedData);\nfor (const [fileKey, file] of Object.entries(files)) {\n    body.append(fileKey, file);\n}\n// eg. using a presto Endpoint\nawait myEndpoint.execute({\n    body,\n    headers: {\n        // Remove default content type from endpoint (eg. json)\n        \'Content-Type\': undefined,\n        \'X-MultiPart-JSON\': true,\n    },\n});\n```\n\n#### Renderers\n\n##### CamelCaseJSONRenderer\n\nRenderer that recursively turns underscore-cased keys into camel-cased keys.\nThis can be set globally on the [DEFAULT_RENDERER_CLASSES](https://www.django-rest-framework.org/api-guide/settings/#default_renderer_classes)\nsetting or on a ViewSet on the `renderer_classes` property.\n\n### Auth\n\n#### MinimalModelBackend\n\n* `allianceutils.auth.backends.MinimalModelBackend`\n    * Replaces the built-in django [ModelBackend](https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.backends.ModelBackend)\n    * Provides django model-based authentication\n    * Removes the default authorization (permissions checks) except for checking `is_superuser` \n\n#### ProfileModelBackend\n\n* Backends for use with [GenericUserProfile](#GenericUserProfile); see code examples there\n* `allianceutils.auth.backends.ProfileModelBackendMixin` - in combo with [AuthenticationMiddleware](https://docs.djangoproject.com/en/stable/ref/middleware/#django.contrib.auth.middleware.AuthenticationMiddleware) will set user profiles on `request.user`  \n    * ~`allianceutils.auth.backends.ProfileModelBackend`~ - convenience class combined with case insensitive username & default django permissions backend\n        * this depended on [`authtools`](https://django-authtools.readthedocs.io/en/latest/) which appears to have been\n          abandoned and does not work with django >= 3.\n          If using django 3 then we recommended that you create your own backend in your app:\n          ```python\n            class ProfileModelBackend(ProfileModelBackendMixin, MinimalModelBackend):\n                # you\'ll need to implement case insensitivity either here or in the User Model  \n                pass\n          ```\n\n### Decorators\n\n#### gzip_page_ajax\n\n* Smarter version of django\'s [gzip_page](https://docs.djangoproject.com/en/stable/topics/http/decorators/#django.views.decorators.gzip.gzip_page):\n    * If settings.DEBUG not set, will always gzip\n    * If settings.DEBUG set, will gzip only if request is an ajax request\n* This allows you to use django-debug-toolbar in DEBUG mode (if you gzip a response then the debug toolbar middleware won\'t run)\n\nExample\n\n```\n\n@allianceutils.views.decorators.gzip_page_ajax\ndef my_view(request: HttpRequest) -> httpResponse:\n    data = {\n        "message": "Hello World",\n    }\n    return django.http.JsonResponse(data) \n\n```\n\n#### method_cache\n\n* Caches the results of a method on the object instance\n* Only works for regular object methods with no arguments other than `self`.\n    * Does not support `@classmethod` or `@staticmethod`\n    * If you want more powerful caching behaviour then you can wrap `cachetools` (examples [here](https://github.com/tkem/cachetools/issues/107))\n* Similar to [`@cached_property`](https://docs.python.org/3/library/functools.html#functools.cached_property) except that it works on methods instead of properties\n* Differs from [`@lru_cache()`](https://docs.python.org/3/library/functools.html#functools.lru_cache) in that\n    * `lru_cache` uses a single cache for each decorated function\n    * `lru_cache` will block garbage collection of values in the cache \n    * A `cache_clear()` method is attached to the function but unlike `lru_cache` it is scoped to an object instance   \n\nUsage\n```python\nclass MyViewSet(ViewSet):\n\n    # ...\n\n    @method_cache\n    def get_object(self):\n        return super().get_object()\n\nobj = MyViewSet()\nobj.get_object() is obj.get_object()\nobj.get_object.cache_clear()   \n```\n\n### Filters\n\n#### MultipleFieldCharFilter\n\nSearch for a string across multiple fields. Requires `django_filters`.\n\n* Usage \n\n```python\nfrom allianceutils.filters import MultipleFieldCharFilter\n\n# ...\n# In your filter set (see django_filters for documentation)\ncustomer = MultipleFieldCharFilter(names=(\'customer__first_name\', \'customer__last_name\'), lookup_expr=\'icontains\')\n```\n\n### Management\n\n#### Commands\n\n##### OptionalAppCommand\n\n* A utility class that extends `django.core.management.base.BaseCommand` and adds optional argument(s) for django apps\n* If app names are passed on the command line `handle_app_config()` will be called with the `AppConfig` for each app otherwise it will be called with every first-party app (as determined by `isort`)\n\n\nExample:\n\n```\nclass Command(allianceutils.management.commands.base.OptionalAppCommand):\n    def add_arguments(self, parser):\n        super().add_arguments(parser)\n        parser.add_argument(\'--type\', choices=(\'name\', \'label\'), default=\'name\')\n\n    def handle_app_config(self, app_config: AppConfig, **options):\n        if options[\'type\'] == \'name\':\n            print(f"Called with {app_config.name}")\n        if options[\'type\'] == \'label\':\n            print(f"Called with {app_config.label}")\n```  \n\n##### print_logging\n\n* Displays the current logging configuration in a hierarchical fashion\n* Requires [`logging_tree`](https://pypi.python.org/pypi/logging_tree) to be installed\n\n#### Checks\n\n* Checks with no configuration are functions that can be passed directly to [register](https://docs.djangoproject.com/en/3.1/topics/checks/)\n* Checks that expect parameters are classes that need to be instantiated\n\nSetting up django hooks:\n\n```python\nfrom django.apps import AppConfig\nfrom django.core.checks import register\nfrom django.core.checks import Tags\n\nfrom allianceutils.checks import check_admins\nfrom allianceutils.checks import check_db_constraints\nfrom allianceutils.checks import CheckExplicitTableNames\nfrom allianceutils.checks import check_git_hooks\nfrom allianceutils.checks import CheckReversibleFieldNames\nfrom allianceutils.checks import CheckUrlTrailingSlash\n\nclass MyAppConfig(AppConfig):\n    # ...\n\n    def ready(self):\n        register(check=check_admins, tags=Tags.admin, deploy=True)\n        register(check=check_db_constraints, tags=Tags.database)\n        register(check=CheckExplicitTableNames(), tags=Tags.models)\n        register(check=check_git_hooks, tags=Tags.admin)\n        register(check=CheckReversibleFieldNames(), tags=Tags.models)\n        register(check=CheckUrlTrailingSlash(expect_trailing_slash=True), tags=Tags.url)        \n```\n\n##### CheckUrlTrailingSlash\n\n* Checks that your URLs are consistent with the `settings.APPEND_SLASH`  \n* Arguments:\n    * `ignore_attrs` - skip checks on url patterns where an attribute of the pattern matches something in here (see example above)\n        * Most relevant attributes of a `RegexURLResolver`:\n            * `_regex` - string used for regex matching. Defaults to `[r\'^$\']`\n            * `app_name` - app name (only works for `include()` patterns). Defaults to `[\'djdt\']` (django debug toolbar)\n            * `namespace` - pattern defines a namespace\n            * `lookup_str` - string defining view to use. Defaults to `[\'django.views.static.serve\']`\n        * Note that if you skip a resolver it will also skip checks on everything inside that resolver\n* Note: If using Django REST Framework\'s [`DefaultRouter`](http://www.django-rest-framework.org/api-guide/routers/#defaultrouter) then you need to turn off `include_format_suffixes`:\n\n```\nrouter = routers.DefaultRouter(trailing_slash=True)\nrouter.include_format_suffixes = False\nrouter.register(r\'myurl\', MyViewSet)\nurlpatterns += router.urls\n```\n\n\n##### check\\_admins\n\n* Checks that `settings.ADMINS` has been properly set in settings files.\n\n##### check\\_git\\_hooks\n\n* Checks that git hookshave been set up, one of:\n  * `.git/hooks` directory has been symlinked to the project\'s `git-hooks`\n  * [`husky`](https://github.com/typicode/husky) hooks have been installed \n* \n\n##### check\\_db\\_constraints\n\n* Checks that all models that specify `db_constraints` in their Meta will generate unique constraint names when truncated by the database.\n\n##### CheckExplicitTableNames\n\n* Checks that all first-party models have `db_table` explicitly defined on their Meta class, and the table name is in lowercase\n* Arguments:\n    * `enforce_lowercase` - check that there are no uppercase characters in the table name\n    * `ignore_labels` - if an app label (eg `silk`) or app_label + model labels (eg `silk.request`)\n        matches something in `ignore_labels` then it will be ignored.\n        * `allianceutils.checks.DEFAULT_TABLE_NAME_CHECK_IGNORE` contains a default list of apps/models to ignore\n        * Can be either a `str` or a regex (anything that contains a `.match()` method) \n\n##### CheckReversibleFieldNames\n\n* Checks that all models have fields names that are reversible with `underscorize`/`camelize`/`camel_to_underscore`/`underscore_to_camel`\n* Arguments:\n    * `ignore_labels` - ignore these apps/models: see `CheckExplicitTableNames`\n\n### Middleware\n\n#### HttpAuthMiddleware\n\n* Middleware to enable basic http auth to block unwanted traffic from search engines and random visitors\n    * Intended to be used on dev / staging servers\n    * Is not a full authorization system: is a single hardcoded username/password and should be used on top of a proper authorization system\n\n* Setup\n    * Add `allianceutils.middleware.HttpAuthMiddleware` to `MIDDLEWARE`.\n    * Add `HTTP_AUTH_USERNAME` and `HTTP_AUTH_PASSWORD` to appropriate setting file, e.g. `settings/production_staging.py`\n        * Remember that you shouldn\'t be hardcoding credentials in code: read content from env vars or file\n\n#### CurrentUserMiddleware\n\n* Middleware to enable accessing the currently logged-in user without a request object.\n    * Assumes that `threading.local` is not shared between requests (an assumption also made by django internationalisation) \n\n* Setup\n    * Add `allianceutils.middleware.CurrentUserMiddleware` to `MIDDLEWARE`.\n\n* Usage\n\n```python\nfrom allianceutils.middleware import CurrentUserMiddleware\n\nuser = CurrentUserMiddleware.get_user()\n```\n\n#### QueryCountMiddleware\n\n* Warns if query count reaches a given threshold\n    * Threshold can be changed by setting `settings.QUERY_COUNT_WARNING_THRESHOLD`\n\n* Usage\n    * Add `allianceutils.middleware.CurrentUserMiddleware` to `MIDDLEWARE`.\n    * Uses the `warnings` module to raise a warning; by default this is suppressed by django\n        * To ensure `QueryCountWarning` is never suppressed  \n\n```python\nwarnings.simplefilter(\'always\', allianceutils.middleware.QueryCountWarning)\n```\n\n* To increase the query count limit for a given request, you can increase `request.QUERY_COUNT_WARNING_THRESHOLD`\n    * Rather than hardcode a new limit, you should increment the existing value\n    * If `request.QUERY_COUNT_WARNING_THRESHOLD` is falsy then checks are disabled for this request \n\n```python\ndef my_view(request, *args, **kwargs):\n    request.QUERY_COUNT_WARNING_THRESHOLD += 10\n    ...\n\n```\n \n\n### Migrations\n\n#### Run SQL function\n* Wrapper to `RunSQL` that reads SQL from a file instead of inline in python\n* The reason you would do this as an external file & function is so that squashed migrations don\'t become unwieldy (django will inline and strip whitespace in the SQL)\n\nUsage:\n```python\nclass Migration(migrations.Migration):\n    # ...\n    operations = [\n        allianceutils.migrations.RunSQLFromFile(\'my_app\', \'0001_intial.sql\'),\n    ]\n```\n\n### Models\n\n#### Utility functions / classes\n\n##### combine_querysets_as_manager\n* `allianceutils.models.combine_querysets_as_manager(Iterable[Queryset]) -> Manager`\n* Replacement for django_permanent.managers.MultiPassThroughManager which no longer works in django 1.8\n* Returns a new Manager instance that passes through calls to multiple underlying queryset_classes via inheritance\n\n##### NoDeleteModel\n\n* A model that blocks deletes in django\n    * Can still be deleted with manual queries\n* Read django docs about [manager inheritance](https://docs.djangoproject.com/en/stable/topics/db/managers/#custom-managers-and-model-inheritance)\n    * If you wish add your own manager, you need to combine the querysets:\n\n```python\nclass MyModel(NoDeleteModel):\n        objects = combine_querysets_as_manager(NoDeleteQuerySet, MyQuerySet)\n```  \n\n#### GenericUserProfile\nAllows you to iterate over a `User` table and have it return a corresponding `Profile` record without generating extra queries\n\nMinimal example:\n\n```python\n# ------------------------------------------------------------------\n# base User model \n\n# If you\'re using django auth instead of authtools, you can just use\n# GenericUserProfileManager instead of having to make your own manager class\nclass UserManager(GenericUserProfileManagerMixin, authtools.models.UserManager):\n    pass\n\nclass User(GenericUserProfile, authtools.models.AbstractEmailUser):\n    objects = UserManager()\n    profiles = UserManager(select_related_profiles=True)\n    \n    # these are the tables that should be select_related()/prefetch_related()\n    # to minimise queries\n    related_profile_tables = [\n        \'customerprofile\',\n        \'adminprofile\',\n    ]\n\n    def natural_key(self):\n        return (self.email,)\n        \n    # the default implementation will iterate through the related profile tables\n    # and return the first profile it can find. If you have custom logic for\n    # choosing the profile for a user then you can do that here\n    #\n    # You would normally not access this directly but instead use the`.profile`\n    # property that caches the return value of `get_profile()` and works\n    # correctly for both user and profile records  \n    def get_profile(self) -> Model:\n        # custom logic\n        if datetime.now() > datetime.date(2000,1,1):\n            return self\n        return super().get_profile()\n\n\n# ------------------------------------------------------------------\n# Custom user profiles\nclass CustomerProfile(User):\n    customer_details = models.CharField(max_length=191)\n\n\nclass AdminProfile(User):\n    admin_details = models.CharField(max_length=191)\n\n# ------------------------------------------------------------------\n# Usage:\n\n# a list of User records\nusers = list(User.objects.all())\n\n# a list of Profile records: 1 query\n# If a user has no profile then you get the original User record back\nprofiles = list(User.profiles.all())\n\n# we can explicitly perform the transform on the queryset\nprofiles = list(User.objects.select_related_profiles().all())\n\n# joining to profile tables: 1 query\n# This assumes that RetailLocation.company.manager is a FK ref to the user table\n# The syntax is a bit different because we can\'t modify the query generation\n# in an unrelated table \nqs = RetailLocation.objects.all()\nqs = User.objects.select_related_profiles(qs, \'company__manager\')\nlocation_managers = list((loc, loc.company.manager.profile) for loc in qs.all())\n```\n\n* There is also an authentication backend that will load profiles instead of just User records\n* If the `User` model has no `get_profile()` method then this backend is equivalent to the built-in django `django.contrib.auth.backends.ModelBackend`\n\n```python\n# ------------------------------------------------------------------\n# Profile authentication middleware\nAUTH_USER_MODEL = \'my_site.User\'\nAUTHENTICATION_BACKENDS = [\n    \'allianceutils.auth.backends.ProfileModelBackend\',\n]\n\n\ndef my_view(request):\n    # standard django AuthenticationMiddleware will call the authentication backend\n    profile = request.user  \n    return HttpResponse(\'Current user is \' + profile.username)\n\n```\n\n* Limitations:\n    * Profile iteration does not work with `.values()` or `.values_list()`\n    \n#### raise_validation_errors\n\n* The `raise_validation_errors` context manager enables cleaner code for constructing validation\n    * [Django documentation](https://docs.djangoproject.com/en/stable/ref/models/instances/#django.db.models.Model.clean) recommends raising a `ValidationError` when you encounter a problem\n    * This creates a poor user experience if there are multiple errors: the user only sees the first error and has to resubmit a form multiple times to fix problems\n* `raise_validation_errors` accepts an (optional) function to wrap\n    * The context manager returns a `ValidationError` subclass with an `add_error` function that follows the same rules as `django.forms.forms.BaseForm.add_error`\n    * If the wrapped function raises a `ValidationError` then this will be merged into the `ValidationError` returned by the context manager\n    * If the wrapped function raises any other exception then this will not be intercepted and the context block will not be executed \n    * At the end of a block,\n        * If code in the context block raised an exception (including a `ValidationError`) then this will not be caught\n        * If `ValidationError` the context manager returned has any errors (either from `ve.add_error()` or from the wrapped function) then this will be raised \n\n```\n    def clean(self):\n        with allianceutils.models.raise_validation_errors(super().clean) as ve:\n            if some_condition:\n                ve.add_error(None, \'model error message\')\n            if other_condition:\n                ve.add_error(\'fieldname\', \'field-specific error message\')\n            if other_condition:\n                ve.add_error(None, {\n                    \'fieldname1\': field-specific error message\',\n                    \'fieldname2\': field-specific error message\',\n                })\n            if something_bad:\n                raise RuntimeError(\'Oh no!\') \n            \n            # at the end of the context, ve will be raised if it contains any errors\n            #   - unless an exception was raised in the block (RuntimeError example above) in which case\n            #     the raised exception will take precedence\n```\n\n* Sometimes you already have functions that may raise a `ValidationError` and `add_error()` will not help\n    * The `capture_validation_error()` context manager solves this problem\n    * Note that due to the way context managers work, each potential `ValidationError` needs its own with `capture_validation_error` context \n\n```\n    def clean(self):\n        with allianceutils.models.raise_validation_errors() as ve:\n             with ve.capture_validation_error():\n                 self.func1()\n             with ve.capture_validation_error():\n                 self.func2()\n             with ve.capture_validation_error():\n                 raise ValidationError(\'bad things\')\n            # all raised ValidationErrors will be collected, merged and raised at the end of this block\n```\n\n### Rules\n\n* Utility functions that return predicates for use with [django-rules](https://github.com/dfunckt/django-rules)\n\n```\nfrom allianceutils.rules import has_any_perms, has_perms, has_perm\n\n# requires at least 1 listed permission\nrules.add_perm(\'northwind.publish_book\', has_any_perms(\'northwind.is_book_author\', \'northwind.is_book_editor\'))\n\n# requires listed permission\nrules.add_perm(\'northwind.unpublish_book\', has_perm(\'northwind.is_book_editor\'))\n\n# requires all listed permissions\nrules.add_perm(\'northwind.sublicense_book\', has_perms(\'northwind.is_book_editor\', \'northwind.can_sign_contracts\'))\n\n```  \n\n### Serializers\n\n#### JSON Ordered\n\n* A version of django\'s core json serializer that outputs field in sorted order\n* The built-in one uses a standard `dict` with completely unpredictable order which causes json diffs to show spurious changes\n\n* Setup\n    * Add to `SERIALIZATION_MODULES` in your settings\n    * This will allow you to do fixture dumps with `--format json_ordered`\n    * Note that django treats this as the file extension to use\n\n```python\nSERIALIZATION_MODULES = {\n    \'json_ordered\': \'allianceutils.serializers.json_ordered\',\n}\n```\n\n### Template Tags\n\n#### render_entry_point\n\n* Replaces old usage of [django-webpack-loader](https://github.com/ezhome/django-webpack-loader)\n   * At time of writing django-webpack-loader does not have a stable release that [works with webpack 4](https://github.com/owais/django-webpack-loader/issues/218)\n   * Worked at bundle level rather than entry point. See below for how we embed tags based on entry point.\n* Reads JSON files generated by [EntryPointBundleTracker](https://gitlab.internal.alliancesoftware.com.au/alliance/webpack-dev-utils/) and embeds the required bundles in the page\n   * Will output tags for all resources of the specified type. eg. Given JSON structure of:\n   ```json\n    {\n      "status": "done",\n      "entrypoints": {\n        "admin": [\n          {\n            "name": "runtime.bundle.js",\n            "contentHash": "e2b781da02d36dad3aff"\n          },\n          {\n            "name": "common.bundle.js",\n            "contentHash": "639269b921c8cf869c5f"\n          },\n          {\n            "name": "common.bundle.css",\n            "contentHash": "d60a0fa36613ea58a23d"\n          },\n          {\n            "name": "admin.bundle.js",\n            "contentHash": "c78fb252d4e00207afef"\n          }\n        ]\n      },\n      "publicPath": "/assets/"\n    }\n   ```\n   \n   Output for `{% render_entry_point \'admin\' \'js\' %}`:\n\n   ```html\n   <script type="text/javascript" src="/assets/runtime.bundle.js?e2b781da02d36dad3aff"></script>\n   <script type="text/javascript" src="/assets/common.bundle.js?639269b921c8cf869c5f"></script>\n   <script type="text/javascript" src="/assets/admin.bundle.js?c78fb252d4e00207afef"></script>\n   ```\n   \n   Output for `{% render_entry_point \'admin\' \'css\' %}`:\n\n   ```html\n   <link type="text/css" href="/assets/common.bundle.css?d60a0fa36613ea58a23d" rel="stylesheet" />\n   ```\n* As an entry point maps to a single HTML file it\'s expected you would only use this tag for a single entry point on a page but generally would call it for both `js` and `css`\n* Arguments\n  * `entry_point_name` - Name of the entry point. This should match one of the entries to \'entry\' in the webpack config.\n  * `resource_type` - The resource type to embed; either `js` or `css`.\n* Optional Arguments\n  * `attrs` - String representing extra attributes to pass to the HTML tag\n  * `config=\'DEFAULT\'` - String index into the settings `WEBPACK_LOADER` dict. Defaults to \'DEFAULT\'.\n* Config\n  * Configuration can be specified via the `WEBPACK_LOADER` setting. This is a dict indexed by the config name (defaults to \'DEFAULT\')\n  * Options\n    * `STATS_FILE` - the path to the stats file to read\n    * `INCLUDE_QUERY_HASH` - whether to include the content hash in the query string. Defaults to `true`.\n    * `BASE_URL` - a URL to prepend to all chunks when rendered. This can be used when files are stored on a different host (eg. CDN).\n\n* Example Usage\n\n```html\n{% load alliance_webpack %}\n<html>\n<head>\n  {% render_entry_point \'app\' \'css\' %}\n</head>\n<body>\n  \n  ...\n  \n  {% if DEBUG %}\n    {# See https://reactjs.org/docs/cross-origin-errors.html #}\n    {% render_entry_point entry_point \'js\' attrs="crossorigin" %}\n  {% else %}\n    {% render_entry_point entry_point \'js\' %}\n  {% endif %}\n</body>\n</html>\n```\n\n#### default_value\n\n* Sets default value(s) on the context in a template\n* This is useful because some built-in django templates raise warnings about unset variables (eg `is_popup` in the django admin template)\n* Note that some tags (eg `with`) save & restore the context state; if done inside such a template tag `default_value` will not persist when the state is restored \n\n```html\n{% load default_value %}\n{{ default_value myvar1=99 myvar2=myvar1|upper }}\n{{ myvar1 }} {{ myvar2 }}\n```\n\n### Util\n\n#### add_autoreload_extra_files\n\n* Adds files to the autoreloader watch list\n    * Works with both the built-in [`runserver`](https://docs.djangoproject.com/en/stable/ref/django-admin/#runserver)\n      and [`runserver_plus`](https://django-extensions.readthedocs.io/en/latest/runserver_plus.html) from `django-extensions`\n    * If `DEBUG` is not enabled then this will do nothing\n    * This should be called from inside the\n      [`ready()`](https://docs.djangoproject.com/en/stable/ref/applications/#django.apps.AppConfig.ready) method of\n      an [`AppConfig`](https://docs.djangoproject.com/en/stable/ref/applications/#configuring-applications) \n  \n```python\nclass MyAppConfig(AppConfig):\n    def ready(self):\n        extra_files = [\n          "/data/file.csv",\n        ]\n        add_autoreload_extra_files(extra_files)\n```\n\n#### camelize\n\n* Better version of [djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case)\n    * DRF-CC camel cases every single key in the data tree.\n* These functions allow you to indicate that certain keys are data, not field names\n\n\n```python\ntree = {\n    "first_name": "Mary",\n    "last_name": "Smith",\n    "servers": {\n        "server_west.mycompany.com": {\n            \'user_accounts\': {\n                \'mary_smith\': {\n                    \'home_dir\': \'/home/mary_smith\',\n                },\n            },\n        },\n    },\n}\n# the keys at tree[\'servers\'] and tree[\'servers\'][\'serve_west.mycompany.com\'][\'user_accounts\'] will not be camel cased\noutput_tree = allianceutils.util.camelize(tree, ignore=[\'servers\', \'servers.*.user_accounts\'])\noutput_tree == {\n    "firstName": "Mary",\n    "lastName": "Smith",\n    "servers": {\n        "server_west.mycompany.com": {\n            \'userAccounts\': {\n                \'mary_smith\': {\n                    \'home_dir\': \'/home/mary_smith\',\n                },\n            },\n        },\n    },\n}\n\n```\n\n* `allianceutils.util.camelize(data, ignores)` - underscore case => camel case a json tree of data\n* `allianceutils.util.underscorize(data, ignores)` - camel case => underscore case a json tree of data\n* `allianceutils.util.camel_to_underscore(str)` - underscore case => camel case a string\n* `allianceutils.util.underscore_to_camel(str)` - camel case => underscore case a string\n* It is assumed that words will not begin with numbers:\n    * `zoo_foo99_bar` is okay\n    * `zoo_foo_99bar` will result in an irreversible transformation (`zooFoo99bar` => `zoo_foo99_bar`) \n\n#### get_firstparty_apps\n\n`util.get_firstparty_apps` can be used to retrieve app_configs considered to be first party, ie, all that does not come from a third party package.\nThis is beneficial when you want to write your own checks by excluding things you dont really care - a sample usage can be found inside \'checks.py\', or\nused as such:\n\n```python\n\nfrom allianceutils.util import get_firstparty_apps\n\napp_configs = get_firstparty_apps()\nmodels_to_be_checked = {}\n\nfor app_config in app_configs:\n    models_to_be_checked.update({\n        model._meta.label: model\n        for model\n        in app_config.get_models()\n    })\n```\n\n#### python_to_django_date_format\n\n* Converts a python [strftime/strptime](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior) datetime format string into a [django template/PHP](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#std:templatefilter-date) date format string\n* Codes with no equivalent will be dropped\n\nExample:\n```python\nallianceutils.util.date.python_to_django_date_format("%Y%m%d %H%M%S")\n# returns "Ymd His"\n```\n\n#### retry_fn\n\n* Repeatedly (up to a hard limit) call specified function while it raises specified exception types or until it returns\n\n```python\nfrom allianceutils.util import retry_fn\n\n# Generate next number in sequence for a model\n# Number here has unique constraint resulting in IntegrityError being thrown\n# whenever a duplicate is added. can be useful for working around mysql\'s lack\n# of sequences\ndef generate_number():\n    qs = MyModel.objects.aggregate(last_number=Max(F(\'card_number\')))\n    next_number = (qs.get(\'last_card_number\') or 0) + 1\n    self.card_number = card_number\n    super().save(*args, **kwargs)\nretry_fn(generate_number, (IntegrityError, ), 10)\n```\n\n## Experimental\n\n* These are experimental and may change without notice\n    * `document_reverse_accessors` management command  \n\n## Changelog\n\nSee [CHANGELOG.md](CHANGELOG.md)\n\n## Development\n\n### Release Process\n\n#### Poetry Config\n* Add test repository\n    * `poetry config repositories.testpypi https://test.pypi.org/legacy/`\n    * Generate an account API token at https://test.pypi.org/manage/account/token/\n    * `poetry config pypi-token.testpypi ${TOKEN}`\n        * On macs this will be stored in the `login` keychain at `poetry-repository-testpypi`\n* Main pypi repository\n    * Generate an account API token at https://pypi.org/manage/account/token/\n    * `poetry config pypi-token.pypi ${TOKEN}`\n        * On macs this will be stored in the `login` keychain at `poetry-repository-pypi`\n\n#### Publishing a New Release\n    * Update CHANGELOG.md with details of changes and new version\n    * Run `bin/build.py`. This will extract version from CHANGELOG.md, bump version in `pyproject.toml` and generate a build for publishing\n    * Tag with new version and update the version branch:\n        * `ver=$( poetry version --short ) && echo "Version: $ver"`\n        * `git tag v/$ver`\n        * `git push --tags`\n    * To publish to test.pypi.org\n        * `poetry publish --repository testpypi`\n    * To publish to pypi.org\n        * `poetry publish`\n\n\n',
    'author': 'Alliance Software',
    'author_email': 'support@alliancesoftware.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AllianceSoftware/django-allianceutils/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
