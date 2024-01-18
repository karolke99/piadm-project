import vtk

class ModelViewer():
    def __init__(self, background_color, model_color, working_dir, smoothing_enabled=False, smoothing_value=1.0,
                 median_enabled=False, median_value=2):
        self.background_color = background_color
        self.model_color = model_color
        self.working_dir = working_dir
        self.smoothing_enabled = smoothing_enabled
        self.smoothing_value = smoothing_value
        self.median_enabled = median_enabled
        self.median_value = median_value

        self.iso_value = 100  # Initial ISO value

        self.volume = vtk.vtkImageData()
        self.colors = vtk.vtkNamedColors()

        self.vtk_image = self.dicom_to_vtk(self.volume)

        self.surface = vtk.vtkMarchingCubes()
        self.surface.SetInputData(self.volume)
        self.surface.ComputeNormalsOn()

        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(self.background_color)

        self.render_window = vtk.vtkRenderWindow()
        self.render_window.AddRenderer(self.renderer)
        self.render_window.SetWindowName('Marching Cubes')

        self.interactor = vtk.vtkRenderWindowInteractor()

        self.iso_slider = vtk.vtkSliderWidget()
        self.iso_slider.SetInteractor(self.interactor)
        self.iso_slider.SetRepresentation(self.create_slider_representation())
        self.iso_slider.SetAnimationModeToAnimate()
        self.iso_slider.AddObserver("InteractionEvent", self.update_iso_value)

        self.surface.SetValue(0, self.iso_value)

        self.interactor.SetRenderWindow(self.render_window)

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection((self.surface.GetOutputPort()))
        self.mapper.ScalarVisibilityOff()

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetColor(self.model_color)

        self.renderer.AddActor(self.actor)

        self.renderer.AddActor(self.iso_slider.GetRepresentation())
        self.iso_slider.On()

        self.render_window.Render()
        self.interactor.Start()

    def create_slider_representation(self):
        slider_rep = vtk.vtkSliderRepresentation2D()
        slider_rep.SetMinimumValue(0)
        slider_rep.SetMaximumValue(1500)
        slider_rep.SetValue(self.iso_value)
        slider_rep.SetTitleText("ISO Value")
        slider_rep.GetSliderProperty().SetColor(1, 1, 1)
        slider_rep.GetSliderProperty().SetLineWidth(2)
        slider_rep.GetTubeProperty().SetColor(1, 1, 1)
        slider_rep.GetTubeProperty().SetLineWidth(1)
        slider_rep.GetLabelProperty().SetColor(1, 1, 1)

        slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
        slider_rep.GetPoint1Coordinate().SetValue(0.1, 0.02)
        slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
        slider_rep.GetPoint2Coordinate().SetValue(0.9, 0.02)

        return slider_rep

    def update_iso_value(self, obj, event):
        slider_value = int(obj.GetRepresentation().GetValue())
        if slider_value != self.iso_value:
            self.iso_value = slider_value
            self.surface.SetValue(0, self.iso_value)
            self.render_window.Render()
    def dicom_to_vtk(self, volume):
        reader = vtk.vtkDICOMImageReader()
        reader.SetDirectoryName(self.working_dir)
        reader.Update()

        if self.median_enabled:
            tmp = reader.GetOutput()
            reader = vtk.vtkImageMedian3D()
            reader.SetInputData(tmp)
            reader.SetKernelSize(self.median_value, self.median_value, self.median_value)
            reader.Update()

        if self.smoothing_enabled:
            tmp = reader.GetOutput()
            reader = vtk.vtkImageGaussianSmooth()
            reader.SetInputData(tmp)
            reader.SetDimensionality(3)
            reader.SetStandardDeviation(self.smoothing_value)
            reader.Update()

        image_data = volume.DeepCopy(reader.GetOutput())
        return image_data
