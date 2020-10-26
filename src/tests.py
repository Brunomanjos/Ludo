# Testes automatizados
# Atualizado: 26/10/2020
# autor: Bruno Messeder dos Anjos

import inspect
import unittest

import tests

__all__ = []


def run_tests():
    """
    Roda todos os testes que estão em '/tests'
    """

    loader = unittest.TestLoader()

    test_classes = inspect.getmembers(
        tests, lambda member: inspect.isclass(member) and issubclass(member, unittest.TestCase))

    suites = []

    for class_name, test_case in test_classes:
        suites.append(loader.loadTestsFromTestCase(test_case))
        print("Caso de Teste:", class_name)

    unittest.TextTestRunner().run(unittest.TestSuite(suites))


if __name__ == '__main__':
    run_tests()
