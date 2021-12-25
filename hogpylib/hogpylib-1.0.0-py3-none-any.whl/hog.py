import numpy as np
from skimage import color, draw
from typing import Tuple, Dict


class HistogramOfGradients:
    def __init__(self, num_of_bins: int = 9,
                 pixels_per_cell: (int, int) = (8, 8),
                 cells_per_block: (int, int) = (1, 1),
                 visualise: bool = False,
                 feature_vector: bool = False) -> None:
        self.num_of_bins = num_of_bins
        self._max_angle = 180
        self.angular_bin_width = self._max_angle / self.num_of_bins
        self.pixels_per_cell = pixels_per_cell
        self.cells_per_block = cells_per_block
        self.visualise = visualise
        self.feature_vector = feature_vector

    def compute_features(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract HOG features
        :param image: input image
        :return: HOG feature, HOG image map
        """
        if len(image.shape) == 3:
            img = color.rgb2gray(image)
        else:
            img = image

        im_h, im_w = img.shape
        gx, gy = self._compute_gradient(img)
        c_row, c_col = self.pixels_per_cell
        b_row, b_col = self.cells_per_block

        magnitudes = np.hypot(gx, gy)
        orientations = np.rad2deg(np.arctan2(gy, gx)) % self._max_angle

        num_cells_x = int(im_w // c_row)
        num_cells_y = int(im_h // c_col)

        num_blocks_x = int(num_cells_x - b_row) + 1
        num_blocks_y = int(num_cells_y - b_col) + 1

        hog_cells = np.zeros((num_cells_y, num_cells_x, self.num_of_bins))

        # Compute HOG of each cell
        for i in range(0, num_cells_y):
            for j in range(0, num_cells_x):
                magnitudes_patch = magnitudes[i * c_col: (i + 1) * c_col, j * c_col: (j + 1) * c_row]
                orientations_patch = orientations[i * c_col: (i + 1) * c_col, j * c_col: (j + 1) * c_row]

                hog_cells[i, j] = self._compute_hog_per_cell(magnitudes_patch,
                                                             orientations_patch)

        hog_blocks_normalized = np.zeros((num_blocks_y, num_blocks_x, self.num_of_bins * b_row * b_col))

        # Normalize HOG by block
        for id_y in range(0, num_blocks_y):
            for id_x in range(0, num_blocks_x):
                hog_block = hog_cells[id_y:id_y + b_col, id_x:id_x + b_row].ravel()
                hog_blocks_normalized[id_y, id_x] = self._normalise_vector(hog_block)
        hog_features = hog_blocks_normalized
        if self.feature_vector:
            hog_features = hog_features.ravel()

        hog_image = None
        if self.visualise:
            hog_image = self._render_hog_image(hog_cells, img.shape)
        return hog_features, hog_image

    @staticmethod
    def _compute_gradient(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute gradient of an image by rows and columns using Forward and Backward difference at edges
        and Central difference for the rest
        :param image: input image of type np.ndarray
        :return: Gradients of image in X and Y direction
        """
        gx = np.zeros_like(image)
        gy = np.zeros_like(image)

        # Central difference
        gx[:, 1:-1] = (image[:, 2:] - image[:, :-2]) / 2
        gy[1:-1, :] = (image[2:, :] - image[:-2, :]) / 2

        # Forward difference
        gx[:, 0] = image[:, 1] - image[:, 0]
        gy[0, :] = image[1, :] - image[0, :]

        # Backward difference
        gx[:, -1] = image[:, -1] - image[:, -2]
        gy[-1, :] = image[-1, :] - image[-2, :]

        # gy, gx = np.gradient(image) # this is built in numpy function to compute gradient
        assert gx.shape == gy.shape
        return gx, gy

    def _compute_hog_per_cell(self, magnitudes: np.ndarray, orientations: np.ndarray) -> np.ndarray:
        """
        Compute 1 HOG feature of a cell. Return a row vector of size `n_orientations`
        :param magnitudes: Gradient magnitude image
        :param orientations: Gradient orientation image
        :return: hog features per cell
        """
        assert orientations.shape == magnitudes.shape
        hog_feature = np.zeros(self.num_of_bins)
        for i in range(orientations.shape[0]):
            for j in range(orientations.shape[1]):
                bin_map = self._calculate_value_of_bins(magnitudes[i, j], orientations[i, j])
                for bin_index in bin_map:
                    hog_feature[bin_index] += bin_map[bin_index]
        return hog_feature / (magnitudes.shape[0] * magnitudes.shape[1])

    def _render_hog_image(self, hog_cells: np.ndarray, hog_image_shape: Tuple[int, int]) -> np.ndarray:
        """
        Render HOG feature image map
        :param hog_cells: Computed HOG features of dim: (M , N, B), M x N is size of input image and B is number of bins
        :param hog_image_shape: (M, N)
        :return: Output HOG image map of size (M, N)
        """
        hog_image = np.zeros(hog_image_shape)
        img_row, img_col = hog_image_shape
        c_row, c_col = self.pixels_per_cell
        num_cells_row, num_cells_col = int(img_row // c_row), int(img_col // c_col)
        orientations = self.num_of_bins

        radius = min(c_row, c_col) // 2 - 1
        orientations_arr = np.arange(orientations)
        # set dr_arr, dc_arr to correspond to midpoints of orientation bins
        orientation_bin_midpoints = (np.pi * (orientations_arr + .5) / orientations)

        dr_arr = radius * np.sin(orientation_bin_midpoints)
        dc_arr = radius * np.cos(orientation_bin_midpoints)

        for r in range(num_cells_row):
            for c in range(num_cells_col):
                for o, dr, dc in zip(orientations_arr, dr_arr, dc_arr):
                    centre = tuple([r * c_row + c_row // 2,
                                    c * c_col + c_col // 2])
                    rr, cc = draw.line(int(centre[0] - dc),
                                       int(centre[1] + dr),
                                       int(centre[0] + dc),
                                       int(centre[1] - dr))
                    hog_image[rr, cc] += hog_cells[r, c, o]
        return hog_image

    @staticmethod
    def _normalise_vector(v: np.ndarray, eps=1e-5) -> np.ndarray:
        """
        Return a normalized vector (which has norm2 as 1)
        @:param v: vector array
        @:param eps: epsilon to prevent zero divide
        @:return normalised vector
        """
        # eps is used to prevent zero divide exceptions (in case v is zero)
        return v / np.sqrt(np.sum(v ** 2) + eps ** 2)

    def _calculate_jth_bin(self, angle: float) -> int:
        """
        Calculate jth bin for a given input angle
        @:param angle: input
        @:return raw bin index
        """
        temp = (angle / self.angular_bin_width) - 0.5
        return np.floor(temp)

    def _calculate_centre_of_jth_bin(self, j: int) -> float:
        """
        Calculate midpoint for a given bin index
        :param j: bin index
        :return: mid point for a bin index
        """
        centre_of_jth_bin = self.angular_bin_width * (j + 0.5)
        return centre_of_jth_bin

    def _calculate_value_of_bins(self, magnitude: float, angle: float) -> Dict[int, float]:
        """
        Calculate Value for bins using voting by bi-linear interpolation
        :param magnitude: magnitude
        :param angle: angle
        :return: Dictionary with bin index as key and  magnitude voting values as corresponding value
        """
        bin_raw_index = self._calculate_jth_bin(angle)

        centre_of_raw_bin_j = self._calculate_centre_of_jth_bin(bin_raw_index)
        centre_of_raw_bin_j_1 = self._calculate_centre_of_jth_bin(bin_raw_index + 1)

        # actual bin index
        bj = int(bin_raw_index % self.num_of_bins)
        bj_1 = int((bin_raw_index + 1) % self.num_of_bins)

        # voting by bi-linear interpolation
        Vj = magnitude * ((centre_of_raw_bin_j_1 - angle) / self.angular_bin_width)
        Vj_1 = magnitude * ((angle - centre_of_raw_bin_j) / self.angular_bin_width)

        return {bj: np.round(Vj, 9), bj_1: np.round(Vj_1, 9)}