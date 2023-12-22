import numpy as np
import vtk
import imageio
import glob


def dicom_to_vtk(volume, dicom_files):

    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(dicom_files)
    reader.Update()
    image_data = volume.DeepCopy(reader.GetOutput())

    return image_data


# def display_image(image_data):
#     render_window = vtk.vtkRenderWindow()
#     render_window.SetWindowName('DICOM Viewer')
#
#     render_window_interactor = vtk.vtkRenderWindowInteractor()
#     render_window_interactor.SetRenderWindow(render_window)
#
#     image_viewer = vtk.vtkImageViewer()
#     image_viewer.SetInputData(image_data)
#     image_viewer.SetRenderWindow(render_window)
#     image_viewer.SetupInteractor(render_window_interactor)
#
#     # image_viewer.SetSliceOrientationToXY()
#
#     render_window.Render()
#     render_window_interactor.Start()


if __name__ == '__main__':
    dicom_path = 'dataset/ct/'

    volume = vtk.vtkImageData()
    colors = vtk.vtkNamedColors()

    vtk_image = dicom_to_vtk(volume, dicom_path)

    surface = vtk.vtkMarchingCubes()
    surface.SetInputData(volume)
    surface.ComputeNormalsOn()
    surface.SetValue(0, 1500)

    renderer = vtk.vtkRenderer()
    renderer.SetBackground(colors.GetColor3d('Black'))

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetWindowName('Marching Cubes')

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection((surface.GetOutputPort()))
    mapper.ScalarVisibilityOff()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('MistyRose'))

    renderer.AddActor(actor)

    render_window.Render()
    interactor.Start()

