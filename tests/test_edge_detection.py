import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from src.edge_detection import get_edges

# src/test_edge_detection.py

class TestGetEdges(unittest.TestCase):
    @patch('src.edge_detection.cv.imread')
    @patch('src.edge_detection.cv.Canny')
    def test_get_edges_basic(self, mock_canny, mock_imread):
        # Arrange
        fake_img = np.ones((10, 10), dtype=np.uint8) * 127
        fake_edges = np.zeros((10, 10), dtype=np.uint8)
        mock_imread.return_value = fake_img
        mock_canny.return_value = fake_edges

        # Act
        result = get_edges('fake_path.jpg', threshold1=50, threshold2=150)

        # Assert
        mock_imread.assert_called_once_with('fake_path.jpg', 0)
        mock_canny.assert_called_once_with(fake_img, 50, 150)
        np.testing.assert_array_equal(result, fake_edges)

    @patch('src.edge_detection.cv.imread', return_value=None)
    def test_get_edges_file_not_found(self, mock_imread):
        with self.assertRaises(AssertionError):
            get_edges('not_found.jpg')

    @patch('src.edge_detection.cv.imread')
    @patch('src.edge_detection.cv.Canny')
    @patch('src.edge_detection.plt.show')
    def test_get_edges_display(self, mock_show, mock_canny, mock_imread):
        fake_img = np.ones((5, 5), dtype=np.uint8) * 100
        fake_edges = np.ones((5, 5), dtype=np.uint8) * 255
        mock_imread.return_value = fake_img
        mock_canny.return_value = fake_edges

        get_edges('any.jpg', display=True)
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()