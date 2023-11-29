import pyglet
import pyglet.gl as GL
import trimesh as tm
import numpy as np
import os
from time import time 
from pathlib import Path

import grafica.transformations as tr

class Body:
    def __init__(self, scale, r, g, b, rotation_speed, shape, satellites=[], dist_from_parent=0, name=''):
        self.name = name
        self.shape = shape
        self.scale = scale
        self.r = r
        self.g = g
        self.b = b
        self.rotation_speed = rotation_speed
        self.satellites = satellites
        self.D = dist_from_parent

    def draw(self, pipeline, parent_transform=tr.identity()):
        transform = parent_transform @ tr.rotationY(self.rotation_speed*time()) @ tr.translate(self.D, 0, 0)

        pipeline["view_transform"] = (transform @ tr.uniformScale(self.scale)).reshape(16, 1, order="F")
        pipeline["r"] = self.r
        pipeline["g"] = self.g
        pipeline["b"] = self.b
        
        self.shape.draw(pyglet.gl.GL_TRIANGLES)

        for s in self.satellites:
            if(self.name == "moon"):
                print(transform)
            s.draw(pipeline, transform)


# Nota:
# Queremos usar el código que está en el módulo grafica
# ubicado en la raíz del repositorio. 
# como ejecutamos el código desde esa raíz, tenemos que agregar
# el módulo a las rutas de búsqueda de módulos del intérprete de Python
# lo ideal sería instalar el módulo gráfica como una biblioteca
# pero no es una biblioteca aún :)
import sys
if sys.path[0] != '':
    sys.path.insert(0, '')

# ahora sí podemos importar funcionalidad desde grafica
import grafica.transformations as tr


if __name__ == "__main__":
    window = pyglet.window.Window(960, 960)
    pyglet.graphics.glEnable(pyglet.graphics.GL_DEPTH_TEST)

    sphere = tm.load("assets/Sphere_Shape.stl")

    # esta parte es igual al ejemplo hello_opengl.
    # sin embargo, el vertex program es ligeramente diferente
    # porque ahora tiene como parámetro una transformación
    with open(Path(os.path.dirname(__file__)) / "shaders/vertex_program.glsl") as f:
        vertex_source_code = f.read()

    with open(Path(os.path.dirname(__file__)) / "shaders/fragment_program.glsl") as f:
        fragment_source_code = f.read()

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    sphere_vertex_list = tm.rendering.mesh_to_vertexlist(sphere)
    sphere_gpu = pipeline.vertex_list_indexed(
        len(sphere_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        sphere_vertex_list[3]
    )
    sphere_gpu.position[:] = sphere_vertex_list[4][1]

    moon = Body(0.0012, 0.6, 0.3, 0.2, 2*np.pi/2, sphere_gpu, dist_from_parent=0.2, name="moon")
    neptune = Body(0.005, 0.0, 0.2, 0.8, 2*np.pi/5, sphere_gpu, satellites=[moon], dist_from_parent=0.7, name="neptune")
    sun = Body(0.02, 0.8, 0.7, 0.3, 0, sphere_gpu, satellites=[neptune])

    # hemos visto que esta función dibuja el mundo dentro del GAME LOOP
    # pero, de cierto modo, es una función estática, no tiene noción del tiempo
    @window.event
    def on_draw():
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        GL.glLineWidth(1.0)

        window.clear()

        pipeline.use()
        
        sun.draw(pipeline)


    # entonces, ¿cómo actualizar el mundo?
    # lo actualizaremos a 60 cuadros por segundo
    # primero definimos la función que utilizaremos
    def update_system(dt, window):
        return

    # aquí le pedimos a pyglet que ejecute nuestra función
    # noten que la ejecución de la actualización del mundo y de su graficación
    # se ejecutan por separado
    pyglet.clock.schedule_interval(update_system, 1 / 60.0, window)

    # let's go justin
    pyglet.app.run(1 / 60.0)
