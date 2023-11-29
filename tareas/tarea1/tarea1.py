# AUTOR: Julieta Ayelli

import pyglet
import pyglet.gl as GL
import trimesh as tm
import numpy as np
import os
from pathlib import Path
from time import time
import grafica.transformations as tr

# clase para controlar la cámara (dónde apunta, su movimiento, etc)
class Camara:
    def __init__(self):
        self.R = 10
        self.h = 1
        self.alpha = 0

    def get_proyeccion(self):
        return tr.perspective(
            45, 1, 0.1, 100
        )

    def update_camara(self, time):
        self.alpha = time * (2 * np.pi) / 5

    def get_camara(self):
        return tr.lookAt(
            np.array([self.R * np.cos(self.alpha), self.R * np.sin(self.alpha), self.h]),
            np.array([0, 0, -0.5]),
            np.array([0, 0, 1])
        )

# clase para posicionar el auto correctamente
class Car():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0.2
        self.alpha = 0
        self.scale = 0.3

    def get_transform(self):
        return tr.matmul([
            tr.translate(self.x, self.y, self.z),
            tr.rotationX(self.alpha),
            tr.uniformScale(self.scale)
        ])

# clase para posicionar las ruedas delanteras correctamente, además de hacerlas
# rotar sobre su propio eje
class FrontWheels():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.alpha = 0
        self.scale = 0.3

    def get_transform(self, time):
        self.alpha = time * (np.pi) / 5
        return tr.matmul([
            tr.translate(1.5*self.scale, -1.3*self.scale, -0.15),
            tr.rotationX(self.alpha),
            tr.translate(-1.5*self.scale, 1.3*self.scale, 1*self.scale),
            tr.uniformScale(self.scale)
        ])

# clase para posicionar las ruedas traseras correctamente, además de hacerlas
# # rotar sobre su propio eje
# class FrontWheels():
class BackWheels():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.alpha = 0
        self.scale = 0.3

    def get_transform(self, time):
        self.alpha = time * (np.pi) / 5
        return tr.matmul([
            tr.translate(-1.5*self.scale, 2.4*self.scale, -0.15),
            tr.rotationX(self.alpha),
            tr.translate(1.5*self.scale, -2.4*self.scale, 1*self.scale),
            tr.uniformScale(self.scale)
        ])

# clase para posicionar las luces del auto correctamente
class Lights():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0.2
        self.alpha = 0
        self.scale = 0.3

    def get_transform(self):
        return tr.matmul([
            tr.translate(self.x, self.y, self.z),
            tr.uniformScale(self.scale)
        ])

# clase para posicionar la plataforma donde descansa el auto correctamente
class Platform():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.alpha = 0
        self.scale = 0.2

    def get_transform(self):
        return tr.matmul([
            tr.rotationX(np.pi/2),
            tr.translate(self.x, -0.4, self.z),
            tr.scale(1.5, 0.05, 1.5)
        ])

# clase para posicionar el garage donde está el auto correctamente
class Garage():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.alpha = 0
        self.scale = 0

    def get_transform(self):
        return tr.matmul([
            tr.translate(0, 0, 0.8),
            tr.scale(1.8, 1.8, 1.3)
        ])


if __name__ == "__main__":
    ## esta es una ventana de pyglet.
    ## le damos la resolución como parámetro
    try:
        ## si queremos más calidad visual (a un costo, claro)
        ## podemos activar antialiasing en caso de que esté disponible
        config = pyglet.gl.Config(sample_buffers=1, samples=4)
        window = pyglet.window.Window(960, 960, config=config)
    except pyglet.window.NoSuchConfigException:
        ## si no está disponible, hacemos una ventana normal
        window = pyglet.window.Window(960, 960)

    camara = Camara()

    # en las siguientes lineas cargo mis modelos
    garage = tm.load("assets\cube.off")

    platform = tm.load("assets\cylinder.off")

    car = tm.load("assets\car.stl")
    car_scale = tr.uniformScale(2.0 / car.scale)
    car_translate = tr.translate(*-car.centroid)

    frontWheels = tm.load(("assets\wheelsFront.stl"))
    frontWheels_translate = tr.translate(*-frontWheels.centroid)

    backWheels = tm.load(("assets\wheelsBack.stl"))
    backWheels_translate = tr.translate(*-backWheels.centroid)

    lights = tm.load("assets\lights.stl")
    lights_translate = tr.translate(*-lights.centroid)

    with open(Path(os.path.dirname(__file__)) / "vertex_program.glsl") as f:
        vertex_source_code = f.read()

    with open(Path(os.path.dirname(__file__)) / "fragment_program.glsl") as f:
        fragment_source_code = f.read()

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    # en las siguientes lineas creo el pipeline con mis modelos
    garage_vertex_list = tm.rendering.mesh_to_vertexlist(garage)
    garage_gpu = pipeline.vertex_list_indexed(
        len(garage_vertex_list[4][1]) // 3, GL.GL_TRIANGLES, garage_vertex_list[3]
    )
    garage_gpu.position[:] = garage_vertex_list[4][1]

    platform_vertex_list = tm.rendering.mesh_to_vertexlist(platform)
    platform_gpu = pipeline.vertex_list_indexed(
        len(platform_vertex_list[4][1]) // 3, GL.GL_TRIANGLES, platform_vertex_list[3]
    )
    platform_gpu.position[:] = platform_vertex_list[4][1]

    car_vertex_list = tm.rendering.mesh_to_vertexlist(car)
    car_gpu = pipeline.vertex_list_indexed(
        len(car_vertex_list[4][1]) // 3, GL.GL_TRIANGLES, car_vertex_list[3]
    )
    car_gpu.position[:] = car_vertex_list[4][1]

    lights_vertex_list = tm.rendering.mesh_to_vertexlist(lights)
    lights_gpu = pipeline.vertex_list_indexed(
        len(lights_vertex_list[4][1]) // 3, GL.GL_TRIANGLES, lights_vertex_list[3]
    )
    lights_gpu.position[:] = lights_vertex_list[4][1]

    frontWheels_vertex_list = tm.rendering.mesh_to_vertexlist(frontWheels)
    frontWheels_gpu = pipeline.vertex_list_indexed(
        len(frontWheels_vertex_list[4][1]) // 3, GL.GL_TRIANGLES, frontWheels_vertex_list[3]
    )
    frontWheels_gpu.position[:] = frontWheels_vertex_list[4][1]

    backWheels_vertex_list = tm.rendering.mesh_to_vertexlist(backWheels)
    backWheels_gpu = pipeline.vertex_list_indexed(
        len(backWheels_vertex_list[4][1]) // 3, GL.GL_TRIANGLES, backWheels_vertex_list[3]
    )
    backWheels_gpu.position[:] = backWheels_vertex_list[4][1]

    # creo mis objetos
    plataforma = Platform()
    auto = Car()
    ruedasDel = FrontWheels()
    ruedasTra = BackWheels()
    luces = Lights()
    pared = Garage()

    ## GAME LOOP
    @window.event
    def on_draw():
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        ## GL_LINE => Wireframe
        ## GL_FILL => pinta el interior de cada triángulo
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glLineWidth(1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)

        window.clear()

        camara.update_camara(time())

        pipeline["projection"] = camara.get_proyeccion().reshape(16, 1, order="F")
        pipeline["view"] = camara.get_camara().reshape(16, 1, order="F")

        pipeline.use()

        # pipeline para la plataforma
        pipeline['r'] = 1.0
        pipeline['g'] = 193 / 255
        pipeline['b'] = 117 / 255
        pipeline["transform"] = plataforma.get_transform().reshape(16, 1, order="F")
        platform_gpu.draw(pyglet.gl.GL_TRIANGLES)

        # pipeline para las ruedas delanteras
        pipeline['r'] = 130 / 255
        pipeline['g'] = 127 / 255
        pipeline['b'] = 130 / 255
        pipeline["transform"] = ruedasDel.get_transform(time()).reshape(16, 1, order="F")
        frontWheels_gpu.draw(pyglet.gl.GL_TRIANGLES)

        # pipeline para las ruedas traseras
        pipeline['r'] = 130 / 255
        pipeline['g'] = 127 / 255
        pipeline['b'] = 130 / 255
        pipeline["transform"] = ruedasTra.get_transform(time()).reshape(16, 1, order="F")
        backWheels_gpu.draw(pyglet.gl.GL_TRIANGLES)

        # pipeline para el cuerpo del auto
        pipeline['r'] = 252 / 255
        pipeline['g'] = 192 / 255
        pipeline['b'] = 244 / 255
        pipeline["transform"] = auto.get_transform().reshape(16, 1, order="F")
        car_gpu.draw(pyglet.gl.GL_TRIANGLES)

        # pipeline para las luces
        pipeline['r'] = 1.0
        pipeline['g'] = 1.0
        pipeline['b'] = 1.0
        pipeline["transform"] = luces.get_transform().reshape(16, 1, order="F")
        lights_gpu.draw(pyglet.gl.GL_TRIANGLES)

        # dibujo con líneas, para que se pueda ver a traves del garage
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)

        # pipeline del garage
        pipeline["transform"] = pared.get_transform().reshape(16, 1, order="F")
        garage_gpu.draw(pyglet.gl.GL_TRIANGLES)

    ## entonces, ¿cómo actualizar el mundo?
    ## lo actualizaremos a 60 cuadros por segundo
    ## primero definimos la función que utilizaremos
    def update_system(dt, window):
        return

    ## aquí le pedimos a pyglet que ejecute nuestra función
    ## noten que la ejecución de la actualización del mundo y de su graficación
    ## se ejecutan por separado
    pyglet.clock.schedule_interval(update_system, 1 / 60.0, window)

    ## aquí comienza pyglet a ejecutar su loop.
    pyglet.app.run()
    ##cuando ejecutemos el programa veremos al conejo en Wireframe!

