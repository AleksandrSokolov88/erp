import os

__test_data_dir = "test/data"
__reference_dir = "test/base"

data = [os.path.join(__test_data_dir, file) for file in os.listdir(__test_data_dir)]
reference = [os.path.join(__reference_dir, file) for file in os.listdir(__reference_dir)]
