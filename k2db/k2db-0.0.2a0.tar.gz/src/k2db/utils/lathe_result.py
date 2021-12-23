from k2db.candidate_network import CandidateNetwork

class LatheResult():

    def __init__(self, index_handler,database_handler,data):
        self.index_handler=index_handler
        self.database_handler=database_handler
        self._dict = data

    def show_cjns(self,**kwargs):
        show_graph=kwargs.get('show_graph',True)
        show_sql=kwargs.get('show_sql',False)
        show_df=kwargs.get('show_df',False)
        top_k=kwargs.get('top_k',0)

        for i,json_cn in enumerate(self._dict['candidate_networks']):
            cjn=CandidateNetwork.from_json_serializable(json_cn)

            print(f'{i+1} CJN:')
            if show_graph:
                print(cjn)
            if show_df:
                sql=cjn.get_sql_from_cn(self.index_handler.schema_graph)
                if show_sql:
                    print(f'SQL:\n{sql}\n')
                print(f'Results:')
                df = self.database_handler.get_dataframe(sql)
                display(df)
            print("-"*50)


            if i+1>=top_k and top_k>0:
                break

    def to_dict(self):
        return self._dict
