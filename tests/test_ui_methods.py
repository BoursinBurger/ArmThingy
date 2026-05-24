from ArmThingyUI import ArmThingyUI

from unittest import mock, TestCase


class UITestCase(TestCase):

    @mock.patch.object(ArmThingyUI, '__init__', return_value=None, autospec=True)
    def test_apply_hash_map(self, _):
        """Test ArmThingyUI apply_hash_map """

        # The constructor has been patched out; initialize the ui object with None
        ui = ArmThingyUI(None)

        # Set the hash map
        ui.hash_map = {'123': 'one_two_three',
                       '456': 'four_five_six',
                       '789': 'seven_eight_nine'}

        # Test string hashing
        assert ui.apply_hash_map('123') == 'one_two_three'
        assert ui.apply_hash_map('456') == 'four_five_six'
        assert ui.apply_hash_map('789') == 'seven_eight_nine'

        # Test dictionary hashing
        assert ui.apply_hash_map({'123': 'foo bar baz'}) == {'one_two_three': 'foo bar baz'}
        assert ui.apply_hash_map({'foo bar baz': '456'}) == {'foo bar baz': 'four_five_six'}
        assert ui.apply_hash_map({'789': '789'}) == {'seven_eight_nine': 'seven_eight_nine'}

        # Test list hashing
        assert ui.apply_hash_map(['2', '3', '456', '7', '8']) == ['2', '3', 'four_five_six', '7', '8']
        assert ui.apply_hash_map(['123', '456', '789']) == ['one_two_three', 'four_five_six', 'seven_eight_nine']

        # Test other object passthru and non-hashing of non-matching strings
        assert ui.apply_hash_map(123) == 123
        assert ui.apply_hash_map([123, 456, 789]) == [123, 456, 789]
        assert ui.apply_hash_map({'123': 123}) == {'one_two_three': 123}
        assert ui.apply_hash_map(None) is None
        assert ui.apply_hash_map('hello world') == 'hello world'
        assert ui.apply_hash_map('one_two_three') == 'one_two_three'
        assert ui.apply_hash_map({'key': 'value'}) == {'key': 'value'}
        assert ui.apply_hash_map(['1', '2', '3']) == ['1', '2', '3']
