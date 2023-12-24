import numpy as np
import vtk
import glob
from vtkmodules.util import numpy_support


class ModelViewer():
    def __init__(self, background_color, model_color, working_dir):
        self.background_color = background_color
        self.model_color = model_color
        self.working_dir = working_dir

        self.volume = vtk.vtkImageData()
        self.colors = vtk.vtkNamedColors()

        self.vtk_image = self.dicom_to_vtk(self.volume)

        self.surface = vtk.vtkMarchingCubes()
        self.surface.SetInputData(self.volume)
        self.surface.ComputeNormalsOn()
        self.surface.SetValue(0, 1500)

        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(self.background_color)

        self.render_window = vtk.vtkRenderWindow()
        self.render_window.AddRenderer(self.renderer)
        self.render_window.SetWindowName('Marching Cubes')

        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.render_window)

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection((self.surface.GetOutputPort()))
        self.mapper.ScalarVisibilityOff()

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetColor(self.model_color)

        self.renderer.AddActor(self.actor)

        self.render_window.Render()
        self.interactor.Start()

    def dicom_to_vtk(self, volume):
        reader = vtk.vtkDICOMImageReader()
        reader.SetDirectoryName(self.working_dir)
        reader.Update()
        image_data = volume.DeepCopy(reader.GetOutput())
        return image_data

# def dicom_to_vtk(volume, dicom_files):
#
#     reader = vtk.vtkDICOMImageReader()
#     reader.SetDirectoryName(dicom_files)
#     reader.Update()
#     image_data = volume.DeepCopy(reader.GetOutput())
#
#     return image_data

# if __name__ == '__main__':
#     dicom_path = 'dataset/ct/'
#
#     volume = vtk.vtkImageData()
#     colors = vtk.vtkNamedColors()
#
#     vtk_image = dicom_to_vtk(volume, dicom_path)
#
#     surface = vtk.vtkMarchingCubes()
#     surface.SetInputData(volume)
#     surface.ComputeNormalsOn()
#     surface.SetValue(0, 1500)
#
#     renderer = vtk.vtkRenderer()
#     renderer.SetBackground(colors.GetColor3d('Black'))
#
#     render_window = vtk.vtkRenderWindow()
#     render_window.AddRenderer(renderer)
#     render_window.SetWindowName('Marching Cubes')
#
#     interactor = vtk.vtkRenderWindowInteractor()
#     interactor.SetRenderWindow(render_window)
#
#     mapper = vtk.vtkPolyDataMapper()
#     mapper.SetInputConnection((surface.GetOutputPort()))
#     mapper.ScalarVisibilityOff()
#
#     actor = vtk.vtkActor()
#     actor.SetMapper(mapper)
#     actor.GetProperty().SetColor(colors.GetColor3d('MistyRose'))
#
#     renderer.AddActor(actor)
#
#     render_window.Render()
#     interactor.Start()
