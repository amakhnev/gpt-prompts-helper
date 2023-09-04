import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.repo_loader.repository_processor import process_prompt_file, process_repository

class TestRepositoryProcessor(unittest.TestCase):

 # Given source file doesn't exist when processing prompt file then print source not found message
    @patch('os.path.exists', side_effect=[False, False])
    @patch('builtins.print')
    def test_process_prompt_file_givenNoSource_whenProcessing_thenPrintSourceNotFound(self, mock_print, mock_exists):
        expected_path = os.path.join('data_path', 'prompt.txt')
        process_prompt_file('data_path', 'output_path')
        mock_print.assert_called_with(f"Source prompt file not found at {expected_path}")



    # Given target file exists when processing prompt file then print target exists message
    @patch('os.path.exists', return_value=True)
    @patch('builtins.print')
    def test_process_prompt_file_givenTargetExists_whenProcessing_thenPrintTargetExists(self, mock_print, mock_exists):
        expected_path = os.path.join('output_path', 'prompt.txt')
        process_prompt_file('data_path', 'output_path')
        mock_print.assert_called_with(f"Prompt file already exists at {expected_path}")

    # Given source file exists and target doesn't when processing prompt file then create target file
    @patch('os.path.exists', side_effect=[False, True])
    @patch('builtins.print')
    def test_process_prompt_file_givenSourceExistsNoTarget_whenProcessing_thenCreateTarget(self, mock_print, mock_exists):
        m = mock_open(read_data="sample_content")
        with patch('builtins.open', m):
            process_prompt_file('data_path', 'output_path')
        m.assert_any_call(os.path.join('output_path', 'prompt.txt'), 'w')
        handle = m()
        handle.write.assert_called_with("sample_content")


    # Given file in ignore list when processing repository then file not added to output
    @patch('os.walk')  
    @patch('os.path.relpath')
    @patch('src.repo_loader.repository_processor.write_to_output')  # replace 'repository_processor' with your actual module name
    def test_process_repository_givenFileInIgnoreList_whenProcessing_thenNotAddedToOutput(
            self, mock_write_to_output, mock_relpath, mock_os_walk):

        # Mocking directory walk to return a single file
        mock_os_walk.return_value = [('repo_path', None, ['sample_file.txt'])]
        mock_relpath.return_value = 'sample_file.txt'

        # Mocking open function
        m = mock_open()
        with patch('builtins.open', m):
            process_repository('repo_path', ['sample_file.txt'], 'output_path')
        
        # Assert that write_to_output was not called
        mock_write_to_output.assert_not_called()

if __name__ == '__main__':
    unittest.main()
