#!/afs/cern.ch/user/d/dhundhau/miniconda3/envs/py310/bin/python
from datetime import timedelta
import glob
import itertools
import time

import awkward as ak
from progress.bar import IncrementalBar
import uproot
import yaml


class NTupleLoader():

    def __init__(self, version, sample, bundle, tree, branches):
        # TODO bundle rename obj_name
        self._version = version
        self._sample = sample
        self._bundle = bundle
        self._tree = tree
        self._branches = branches
        self._ntuple_path = ""
        self._set_ntuple_path()
        self._final_ak_array = None

    @property
    def parquet_fname(self):
        return self._version + '_' + self._sample + "_" + self._bundle

    def _set_ntuple_path(self):
        """
        Load cfg file to extract path to ntuples.
        """
        with open("cfg.yaml", 'r') as f:
            cfg = yaml.safe_load(f)[self._version][self._sample]
        self._ntuple_path = cfg["ntuple_path"]

    def _concat_array_from_ntuples(self):
        fnames = glob.glob(self._ntuple_path)[:]

        print(f"Loading objects from {len(fnames)} files...")
        bar = IncrementalBar("Progress", max=len(fnames))
        t0 = time.time()

        branches = [self._bundle + x for x in self._branches]
        all_arrays = {x: [] for x in branches}
        for fname in fnames:
            bar.next()
            with uproot.open(fname) as f:
                for branch in branches:
                    br = f[self._tree][branch].arrays(library="ak")[branch]
                    # all_arrays[branch].append(br)
                    all_arrays[branch] = ak.concatenate([all_arrays[branch], br])

        self._final_ak_array = ak.zip(all_arrays)

        t1 = time.time()
        bar.finish()
        print(self._final_ak_array.fields)
        print(f"Loading completed in {timedelta(seconds=round(t1 - t0, 0))}s")

    def _cache_file_exists(self):
        """
        Checks if there is parquet file in tmp
        with the name 'version_sample_bundle.parquet'
        """
        cached_files = glob.glob("tmp/*")
        return False
        return self.parquet_fname + ".parquet" in cached_files

    def _save_array_to_parquet(self):
        ak.to_parquet(
            self._final_ak_array,
            where=f"tmp/{self.parquet_fname}.parquet"
        )

    def load(self):
        if True:  # not (self._cache_file_exists() and self._cache_has_columns()):
            # print("No adequate cache file.")
            self._concat_array_from_ntuples()
            self._save_array_to_parquet()


if __name__ == "__main__":
    with open("cfg.yaml", 'r') as f:
        cfg = yaml.safe_load(f)
    for version, samples in cfg.items():
        for sample, sample_cfg in samples.items():
            for tree, bundle_branches in sample_cfg["trees_branches"].items():
                if tree == "ntuple_path":
                    continue
                for bundle, branches in bundle_branches.items(): 
                    print(tree, bundle)
                    loader = NTupleLoader(
                        version=version,
                        sample=sample,
                        tree=tree,
                        bundle=bundle,
                        branches=branches,
                    )
                    loader.load()

