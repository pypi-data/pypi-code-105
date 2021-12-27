import os
from os import getenv
from os.path import join
from pathlib import Path
from pytest import mark
from datetime import datetime
from testrail_api import TestRailAPI


class TestRail:
    @staticmethod
    def id(*ids: str) -> mark:
        return mark.testrail_ids(ids=ids)

    def _get_status(self, tr: TestRailAPI, case_id: int, test_run_id: int) -> int:
        case = tr.results.get_results_for_case(
            run_id=int(test_run_id),
            case_id=int(case_id),
            limit=1
        )
        if len(case) == 0:
            return 0
        return case[0]['status_id']

    def _get_milestone_id(self, tr: TestRailAPI):
        mls = tr.milestones.get_milestones(project_id=int(getenv('TESTRAIL_PROJECT_ID')))
        for ml in mls:
            if ml['name'] == str(getenv('TESTRAIL_MILESTONE')):
                return ml['id']

    def _get_test_runs(self, tr: TestRailAPI, name: str):
        for run in tr.runs.get_runs(project_id=int(getenv('TESTRAIL_PROJECT_ID')), is_completed=False):
            if name in run['name']:
                return run['id']
        return None

    def create_test_run(self, tr: TestRailAPI) -> int:
        date = datetime.today().strftime('%d.%m.%Y')
        time = datetime.today().strftime('%H:%M:%S')
        name = f"{getenv('TESTRAIL_TITLE_RUN')} {date} {time}"
        ml = self._get_milestone_id(tr=tr)
        if not ml:
            raise ValueError('Milestone с указаным именем не найден')
        lasted_test_run = self._get_test_runs(tr=tr, name=f"{getenv('TESTRAIL_TITLE_RUN')} {date}")
        if lasted_test_run is not None:
            return lasted_test_run
        return tr.runs.add_run(
            project_id=int(getenv('TESTRAIL_PROJECT_ID')),
            name=name,
            milestone_id=ml,
            case_ids=self._get_test_case_ids() if int(getenv('TESTRAIL_AUTOCLOSE_TESTRUN')) == 1 else [],
            include_all=int(getenv('TESTRAIL_AUTOCLOSE_TESTRUN')) == 0
        )['id']

    def _get_test_case_ids(self):
        tests = join(Path(__file__).parent.parent.parent.parent, 'tests')
        test_case_ids = []
        for root, dirs, files in os.walk(tests, topdown=False):
            for name in files:
                if name.split('.')[-1] == 'pyc':
                    continue
                file = open(os.path.join(root, name), 'rb')
                text = str(file.read())
                while text.find("@TestRail.id('") != -1:
                    start_with = text.find("@TestRail.id('") + 15
                    id = text[start_with::].split("')")[0]
                    if id != '' and len(id) > 2:
                        test_case_ids.append(int(id))
                    text = text[start_with::]
        return test_case_ids

    def close_test_run(self, tr: TestRailAPI, run_id: int):
        tr.runs.close_run(run_id=run_id)

    def set_status(self, tr: TestRailAPI, data: dict):
        test_run_id = data['test_run_id']
        case_id = int(str(data['case_id'][1:]))

        if test_run_id is None:
            return

        if self._get_status(tr, case_id, test_run_id) == 5:
            print(f'Тест кейс с ID {data["case_id"]} уже находится в статусе Failed')
            return

        result = tr.results.add_result_for_case(
            run_id=int(test_run_id),
            case_id=int(case_id),
            status_id=int(data['status']),
            elapsed=data['elapsed'],
            comment=data['comment']
        )

        if data.get('screenshot') is not None:
            tr.attachments.add_attachment_to_result(result["id"], data['screenshot'])
