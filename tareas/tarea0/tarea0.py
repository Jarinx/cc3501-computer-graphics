import pyglet
from OpenGL import GL
import numpy as np
import os
from pathlib import Path

#Código del repositorio del curso, "hello_world >> app.py, modificado para
#la tarea 0, eliminando lo que no es necesario

if __name__ == "__main__":
    win = pyglet.window.Window(800, 600)

    #vertices para una "piramide" con vista de plano,
    #se hacen 9 vertices en total para que cada cada tenga su propio color
    vertices = np.array(
        [0.5,-0.5, 0.0, # 0
        -0.5,-0.5, 0.0, # 1
         0.0, 0.0, 0.0, # 2
        -0.5,-0.5, 0.0, # 3
         0.0, 0.5, 0.0, # 4
         0.0, 0.0, 0.0, # 5
         0.0, 0.5, 0.0, # 6
         0.5,-0.5, 0.0, # 7
         0.0, 0.0, 0.0  # 8
        ],
        dtype=np.float32,
    )

    vertex_colors = np.array(
        [1.0, 153 / 255.0, 204 / 255.0,  # 0 - 0, 1 y 2 tienen los mismos colores
         1.0, 153 / 255.0, 204 / 255.0,  # 1
         1.0, 153 / 255.0, 204 / 255.0,  # 2
         1.0, 204 / 255.0, 229 / 255.0,  # 3 - 3, 4 y 5 tienen los mismos colores
         1.0, 204 / 255.0, 229 / 255.0,  # 4
         1.0, 204 / 255.0, 229 / 255.0,  # 5
         1.0, 102 / 255.0, 178 / 255.0,  # 6 - 6, 7 y 8 tienen los mismos colores
         1.0, 102 / 255.0, 178 / 255.0,  # 7
         1.0, 102 / 255.0, 178 / 255.0   # 8
        ],
        dtype=np.float32,
    )

    indices = np.array([0, 1, 2,
                        3, 4, 5,
                        6, 7, 8
                        ], dtype=np.uint32)


    with open(Path(os.path.dirname(__file__)) / "vertex_program.glsl") as f:
        vertex_source_code = f.read()

    with open(Path(os.path.dirname(__file__)) / "fragment_program.glsl") as f:
        fragment_source_code = f.read()

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    #le decimos que tenemos 9 vertices
    gpu_data = pipeline.vertex_list_indexed(9, GL.GL_TRIANGLES, indices)

    gpu_data.position[:] = vertices
    gpu_data.color[:] = vertex_colors

    @win.event
    def on_draw():
        GL.glClearColor(0.5, 0.5, 0.5, 1.0)

        win.clear()

        pipeline.use()

        gpu_data.draw(GL.GL_TRIANGLES)

    pyglet.app.run()
