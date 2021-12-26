__all__ = [
    'Medication',
    'Brand',
    'DrugSet',
    'DistributionForm',
    'get_medication_instances'
]

from ._base import utils, namedtuple

DrugSet = namedtuple('DrugSet', 'drug strength unit')
DistributionForm = namedtuple('DistributionForm', 'quantity dosage_form usage_form', defaults=[None])
DistributionForm.__usage_form__ = lambda self: self.dosage_form if not self.usage_form else self.usage_form

Brand = namedtuple('Brand', 'name drugs sets pharmaceutical recipe usage_form key', defaults=['C', None, None])
Brand.__drugs__ = lambda self: utils.semicolon_split(self.drugs)
Brand.__sets__ = lambda self: utils.semicolon_split(self.sets)

Brand.__presentations__ = lambda self: [utils.list_words(x) for x in utils.semicolon_split(self.sets)]
Brand.__table__ = 'BrandDrug'
Brand.__project__ = 'base'
Brand.__str__ = lambda self: f'{self.name} ({self.pharmaceutical})'

Medication = namedtuple('Medication', 'drugs strengths content recipe name pharmaceutical', defaults=['C', None, None])

Brand.__medications__ = lambda self: [Medication(self.__drugs__(), s[:-1], s[-1], self.recipe, self.name, self.pharmaceutical) for s in self.__presentations__()]

Medication = namedtuple('Medication', 'drugs strengths content recipe name pharmaceutical', defaults=['C', None, None])
Medication.__str__ = lambda self: f'{self.name} ({"+".join(self.drugs)}) {"+".join(self.strengths)} {self.content}'
Medication.__key__ = lambda self: (utils.cammel_case(self.name) + utils.only_digits("".join(self.strengths) + self.content)).replace(' ','').replace('.','')
# aditional semicolon_split(data['drugs'])
Medication.__content__ = lambda self: DistributionForm(*utils.split_digits_and_letters(self.content))
Medication.__strengths__ = lambda self: [utils.split_digits_and_letters(x) for x in self.strengths]
Medication.__drug_sets__ = lambda self: [DrugSet(x[0], x[1][0], x[1][1]) for x in zip(self.drugs, self.__strengths__())]



async def get_medication_instances(conn):
    async with conn.base.ListAll('BrandDrug') as result:
        data = []
        for item in result:
            d = utils.process_branded_drug(item)
            for i in d:
                data.append(Medication(*i))
        return data 