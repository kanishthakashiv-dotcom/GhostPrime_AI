import os

class GhostTestSuite:
    @staticmethod
    def get_data_config(example_type):
        """Maps scenarios to your specific local filenames."""
        data_map = {
            "pandemic": {
                "target_file": "ZIKV.fna", 
                "ghost_file": "DENV.fna",
                "primers": ("GCGTTAATGCAACTGGTGTG", "TCGACCAGATGATCCACAGC")
            },
            "guardian": {
                "target_file": "Pyricularia_oryzae.fna", 
                "ghost_file": "IRGSP_genome.fna",
                "primers": ("GCGCTCGTTTAGCCTCAAGT", "TCGGTCGGCATGTTGTTGAA")
            },
            "auditor": {
                "target_file": "Chlorella_vulgaris.fna", 
                "ghost_file": "GCA_002245835.2.fna",
                "primers": ("ATGCAGTCGACGATGCA", "GGGGGAAAAACCCCC")
            }
        }
        return data_map.get(example_type)

    @staticmethod
    def verify_files(config):
        """Checks if files exist to prevent tracebacks."""
        for key in ['target_file', 'ghost_file']:
            if not os.path.exists(config[key]):
                return False, config[key]
        return True, None
