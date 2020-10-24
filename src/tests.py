# Testes automatizados
# Atualizado: 19/10/2020
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

    for class_name, _ in test_classes:
        print("Caso de Teste:", class_name)

    suites = [loader.loadTestsFromTestCase(test_case) for _, test_case in test_classes]

    unittest.TextTestRunner().run(unittest.TestSuite(suites))


if __name__ == '__main__':
    run_tests()
