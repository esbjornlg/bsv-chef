import pytest
import pytest_cov
import unittest.mock as mock
from unittest.mock import patch
from src.controllers.receipecontroller import ReceipeController 
from static.diets import Diet
recipe = {
    "name": "Banana Bread",
    "diets": [
        "normal", "vegetarian"
    ],
    "ingredients": {
        "Butter": 100,
        "Banana": 4,
        "Sugar": 200,
        "Egg": 1,
        "Vanilla Sugar": 1,
        "Baking Powder": 0.5,
        "Salt": 5,
        "Cinnamon": 10,
        "Flour": 220,
        "Walnuts": 10
    }
}
@pytest.fixture
def sut():
    with patch.object(ReceipeController, 'load_receipes', return_value=recipe):
        mocked_dao = mock.MagicMock()
        sut = ReceipeController(mocked_dao)
        return sut

# add your test case implementation here

@pytest.mark.unit
@pytest.mark.parametrize("available_items", "diet", [({"Butter": 10}, Diet.VEGETARIAN)])
def test_get_receipe_readiness_readiness(sut, available_items, diet):
    with patch('src.util.calculator.calculate_readiness') as mocked_calculate_readiness:
        mocked_calculate_readiness.return_value = 0.1
        validation_result = sut.get_receipe_readiness(receipe, available_items, diet)
        assert validation_result >= 0.1

@pytest.mark.unit
@pytest.mark.parametrize("available_items", "diet", [({"Butter": 10}, Diet.VEGETARIAN)])
def test_get_receipe_readiness_None_RightDiet_InsufficientItems(sut, available_items, diet):
    with patch('src.util.calculator.calculate_readiness') as mocked_calculate_readiness:
        mocked_calculate_readiness.return_value = 0.05
        validation_result = sut.get_receipe_readiness(receipe, available_items, diet)
        assert validation_result is None

@pytest.mark.unit
@pytest.mark.parametrize("available_items", "diet", [({"Butter": 10}, Diet.VEGAN)])
def test_get_receipe_readiness_None_WrongDiet_SufficientItems(sut, available_items, diet):
    with patch('src.util.calculator.calculate_readiness') as mocked_calculate_readiness:
        mocked_calculate_readiness.return_value = 0.5
        validation_result = sut.get_receipe_readiness(receipe, available_items, diet)
        assert validation_result is None

@pytest.mark.unit
@pytest.mark.parametrize("available_items", "diet", [({"Butter": 10}, Diet.VEGAN)])
def test_get_receipe_readiness_None_WrongDiet_InsufficientItems(sut, available_items, diet):
    with patch('src.util.calculator.calculate_readiness') as mocked_calculate_readiness:
        mocked_calculate_readiness.return_value = 0.05
        validation_result = sut.get_receipe_readiness(receipe, available_items, diet)
        assert validation_result is None