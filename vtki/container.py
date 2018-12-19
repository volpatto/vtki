"""
Containers to mimic multi block datasets
"""
import logging
from weakref import proxy

import numpy as np
import vtk
from vtk import vtkMultiBlockDataSet

log = logging.getLogger(__name__)
log.setLevel('CRITICAL')

import vtki
from vtki.utilities import wrap


class MultiBlock(vtkMultiBlockDataSet):
    """
    A container class to hold a set of data sets which can be iterated over.

    This is a very rough prototype... needs a lot of work.
    """

    _is_vtki = True

    def __init__(self, *args, **kwargs):
        super(MultiBlock, self).__init__()
        deep = kwargs.pop('deep', False)

        if len(args) == 1:
            if isinstance(args[0], vtk.vtkMultiBlockDataSet):
                if deep:
                    self.DeepCopy(args[0])
                else:
                    self.ShallowCopy(args[0])


    def plot(self, **args):
        """
        Calls ``add_mesh`` for each element in the multiblock dataset
        """
        p = vtki.Plotter()
        for idx in range(self.GetNumberOfBlocks()):
            data = wrap(self.GetBlock(idx))
            p.add_mesh(data, **args)
        return p.plot()

    def __getitem__(self, index):
        """Get a block by its index"""
        return self.GetBlock(index)

    def __setitem__(self, index, data):
        """Sets a block with a VTK data object"""
        self.SetBlock(index, data)