import logging
from count import buckets_number_obj
from name import bucket_name
from date import bucket_creation_date
from size import buckets_number_size

try:
    def bucket_summarize(buckets):
        dt_criacao = bucket_creation_date(buckets)
        num_obj = buckets_number_obj(buckets)
        size_obj = buckets_number_size(buckets)
        res = dict()

        for key in buckets:
            for x, y, z in [(x, y, z) for x in dt_criacao for y in num_obj for z in size_obj]:
                res[key] = [x, y, z]
        print(res)

except TypeError:
    print('Error' + TypeError)
