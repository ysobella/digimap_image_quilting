# TORIO, Ysobella D.
# Sources:
# https://jmecom.github.io/projects/computational-photography/texture-synthesis/

from base import ImageQuilting, BoxIndeces, QuiltingOutputs

import numpy as np
import cv2
import scipy.ndimage as ndimage
import PIL.Image as Image
import imageio
import os


# SCORE -1 if you imported additional modules


# SUBMISSION: You only need to submit this file 'implementation.py'

# Hint: You could refer to online sources for help as long as you cite it

# Hint: For clues on the implementation logic,
# view 'base.ImageQuiltingRandom'

# SCORE +5 for submitting this file (implementation.py)

# Feel free to add as much helper functions in the class
class ImageQuilting_AlgorithmAssignment(ImageQuilting):

    # SCORE +1 for implementing load image
    def load_image(self, path: str) -> np.ndarray:
        # raise NotImplementedError()
        image = cv2.imread(path)
        if image is None:
            raise ValueError(f"Failed to load image from {path}")
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # return image

    # SCORE +1 for implementing save image
    def save_image(self, path: str, image: np.ndarray):
        # raise NotImplementedError()
        # converting back to BGR for saving
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = Image.fromarray(image)
        image.save(path)

    # SCORE +1 for finding the best matching patch using L2 similarity
    # SCORE +1 for using L2 similarity on the overlap areas only
    def find_matching_texture_patch_indeces(
            self,
            canvas_patch: np.ndarray,
            canvas_indeces: BoxIndeces,
            canvas: np.ndarray,
            block_size: int,
            block_overlap: int
    ) -> BoxIndeces:
        # best_match_indeces = None
        # best_match_score = float('inf')
        #
        # for top in range(0, self.texture_image.shape[0] - block_size, block_size - block_overlap):
        #     for left in range(0, self.texture_image.shape[1] - block_size, block_size - block_overlap):
        #         texture_patch = self.extract_patch(self.texture_image,
        #                                            BoxIndeces(top, top + block_size, left, left + block_size))
        #         score = np.sum((canvas_patch - texture_patch) ** 2)
        #         if score < best_match_score:
        #             best_match_score = score
        #             best_match_indeces = BoxIndeces(top, top + block_size, left, left + block_size)
        #
        # return best_match_indeces

        # texture_height, texture_width, _ = self.texture_image.shape
        # patch_height, patch_width, _ = canvas_patch.shape
        # min_error = float('inf')
        # best_texture_indeces = None
        #
        # for y in range(texture_height - patch_height + 1):
        #     for x in range(texture_width - patch_width + 1):
        #         texture_patch = self.texture_image[y:y + patch_height, x:x + patch_width, :]
        #         error = np.sum(np.square(canvas_patch - texture_patch))
        #         if error < min_error:
        #             min_error = error
        #             best_texture_indeces = BoxIndeces(y, y + patch_height, x, x + patch_width)
        #
        # return best_texture_indeces
        texture_height, texture_width, _ = self.texture_image.shape
        patch_height, patch_width, _ = canvas_patch.shape
        random_y = np.random.randint(0, texture_height - patch_height)
        random_x = np.random.randint(0, texture_width - patch_width)
        return BoxIndeces(
            top=random_y,
            bottom=random_y + patch_height,
            left=random_x,
            right=random_x + patch_width
        )

    # SCORE +1 for finding a 'cut' that minimizes the L2 error
    # SCORE +1 for correctly converting a 'cut' to a 'mask' (Hint: mask is binary)
    # SCORE +1 for returning the correct mask for the initial case (row=0, column=0)
    # SCORE +1 for returning the correct mask for the first row (row=0, colums>1) and the first column (row>1, columns=0)
    # SCORE +1 for returning the correct mask for the other cases (row>1, columns>1)
    def compute_texture_mask(
            self,
            canvas_patch: np.ndarray,
            texture_patch: np.ndarray,
            canvas_indeces: BoxIndeces,
            texture_indeces: BoxIndeces,
            canvas: np.ndarray,
            block_size: int,
            block_overlap: int
    ) -> np.ndarray:
        # raise NotImplementedError()
        # difference between the canvas patch and the texture patch
        # diff = canvas_patch - texture_patch
        # # L2 distance transform of the absolute difference
        # dist_transform = ndimage.distance_transform_edt(np.abs(diff))
        # # best cut -> finding the minimum value in the distance transform
        # best_cut = np.argmin(dist_transform)
        # # best cut to mask conversion
        # mask = np.zeros_like(diff, dtype=bool)
        # mask[best_cut // block_size, best_cut % block_size] = True
        # mask = mask[:, :, 0]
        # return mask

        # overlap_height = min(block_overlap, canvas_patch.shape[0])
        # overlap_width = min(block_overlap, canvas_patch.shape[1])
        # texture_patch_resized = cv2.resize(texture_patch, (canvas_patch.shape[1], canvas_patch.shape[0]))
        # # combined_patch = texture_patch * texture_patch_resized[:, :, np.newaxis] + canvas_patch * (
        # #             1 - texture_patch_resized[:, :, np.newaxis])
        #
        # texture_height, texture_width, _ = texture_patch_resized.shape
        # # mask = np.zeros((texture_height, texture_width))
        # mask = np.zeros_like(texture_patch_resized)
        #
        # # for channel in range(3):  # assuming RGB channels
        # #     mask[:, :, channel] = np.square(
        # #         canvas_patch[:overlap_height, :overlap_width, channel] - texture_patch_resized[:, :, channel])
        #
        # print("Shapes:")
        # print("canvas_patch:", canvas_patch.shape)
        # print("texture_patch_resized:", texture_patch_resized.shape)
        #
        # if canvas_indeces.top == 0 and canvas_indeces.left == 0:
        #     return mask
        #
        # if canvas_indeces.top == 0:
        #     # error_top = np.sum(np.square(canvas_patch - texture_patch_resized[:block_overlap]))
        #     error_top = np.sum(np.square(canvas_patch[:overlap_height, :overlap_width] - texture_patch_resized))
        #     mask[:block_overlap] = 1
        #     for y in range(block_overlap, texture_height):
        #         error = np.sum(np.square(canvas_patch - texture_patch_resized[y:y + block_overlap]))
        #         if error < error_top:
        #             mask[y] = 1
        #             error_top = error
        #     return mask
        #
        # if canvas_indeces.left == 0:
        #     error_left = np.sum(np.square(canvas_patch - texture_patch_resized[:, :block_overlap]))
        #     mask[:, :block_overlap] = 1
        #     for x in range(block_overlap, texture_width):
        #         error = np.sum(np.square(canvas_patch - texture_patch_resized[:, x:x + block_overlap]))
        #         if error < error_left:
        #             mask[:, x] = 1
        #             error_left = error
        #     return mask
        #
        # error_top_left = np.sum(
        #     np.square(canvas_patch[:block_overlap, :block_overlap] - texture_patch_resized[:block_overlap, :block_overlap]))
        # mask[:block_overlap, :block_overlap] = 1
        # for y in range(block_overlap, texture_height):
        #     for x in range(block_overlap, texture_width):
        #         error = np.sum(np.square(
        #             canvas_patch[y:y + block_overlap, x:x + block_overlap] - texture_patch_resized[y:y + block_overlap,
        #                                                                      x:x + block_overlap]))
        #         if error < error_top_left:
        #             mask[y, x] = 1
        #             error_top_left = error
        # return mask
        # --------
        # texture_height, texture_width, _ = texture_patch.shape
        # mask = np.ones((texture_height, texture_width))
        # return mask
        # ------------
        # texture_height, texture_width, _ = texture_patch.shape
        # mask = np.ones((texture_height, texture_width))
        #
        # # Function to create a torn-like mask for the specified edges
        # def create_torn_mask(mask, edge_width):
        #     for i in range(mask.shape[0]):
        #         for j in range(mask.shape[1]):
        #             # For patches in the first column, only mask the top edge
        #             if j == 0 and i < edge_width:
        #                 if np.random.rand() < 0.5:
        #                     mask[i, j] = 0
        #             # For patches in the first row, only mask the left edge
        #             elif i == 0 and j < edge_width:
        #                 if np.random.rand() < 0.5:
        #                     mask[i, j] = 0
        #             # For patches in both the first row and first column, no mask is added
        #             elif i == 0 and j == 0:
        #                 continue
        #     return mask
        #
        # # Apply the torn mask to the specified edges
        # mask = create_torn_mask(mask, block_overlap)
        #
        # return mask
        # -----
        # texture_height, texture_width, _ = texture_patch.shape
        # mask = np.ones((texture_height, texture_width))
        #
        # # Function to create a torn-like mask for the specified edges
        # def create_torn_mask(mask, edge_width):
        #     for i in range(mask.shape[0]):
        #         for j in range(mask.shape[1]):
        #             if i < edge_width:
        #                 # Create a torn effect by randomly setting some pixels to 0
        #                 if np.random.rand() < 0.5:
        #                     mask[i, j] = 0
        #             if j < edge_width:
        #                 # Create a torn effect by randomly setting some pixels to 0
        #                 if np.random.rand() < 0.5:
        #                     mask[i, j] = 0
        #             if i < edge_width and j < edge_width:
        #                 # Create a torn effect by randomly setting some pixels to 0
        #                 if np.random.rand() < 0.5:
        #                     mask[i, j] = 0
        #     return mask
        #
        # # Apply the torn mask to the upper, left, and top-left edges
        # mask = create_torn_mask(mask, block_overlap)
        #
        # return mask
        # -----
        texture_height, texture_width, num_channels = texture_patch.shape
        mask = np.ones((texture_height, texture_width))

        # Initialization topmost-leftmost patch
        if canvas_indeces.top == 0 and canvas_indeces.left == 0:
            return mask

        # Left overlap / Topmost patches
        if canvas_indeces.top == 0:
            path_index = np.random.randint(0, block_overlap)
            for y in range(texture_height):
                mask[y, :path_index] = 0

                random_offset = np.random.choice([1, 0, -1])
                path_index += random_offset
                path_index = np.clip(path_index, 0, block_overlap - 1)

            return mask

        # Top overlap / Leftmost patches
        if canvas_indeces.left == 0:
            path_index = np.random.randint(0, block_overlap)
            for x in range(texture_width):
                mask[:path_index, x] = 0

                random_offset = np.random.choice([1, 0, -1])
                path_index += random_offset
                path_index = np.clip(path_index, 0, block_overlap - 1)
            return mask

        # Left and Top overlap / The other patches
        path_index = np.random.randint(0, block_overlap)
        for y in range(texture_height):
            mask[y, :path_index] = 0

            random_offset = np.random.choice([1, 0, -1])
            path_index += random_offset
            path_index = np.clip(path_index, 0, block_overlap - 1)

        path_index = np.random.randint(0, block_overlap)
        for x in range(texture_width):
            mask[:path_index, x] = 0

            random_offset = np.random.choice([1, 0, -1])
            path_index += random_offset
            path_index = np.clip(path_index, 0, block_overlap - 1)

        return mask
    # SCORE +1 if there are no errors when running the entire algorithm
