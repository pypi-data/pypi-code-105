

class BRtools:

    def is_valid_cpf(cpf: str) -> bool:
        from validate_cpf import is_valid
        return is_valid(cpf)

    def is_valid_cnpj(cnpj: str) -> bool:
        from validate_cnpj import is_valid
        return is_valid(cnpj)