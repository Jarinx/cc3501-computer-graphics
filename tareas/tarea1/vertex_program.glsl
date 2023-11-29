#version 330
in vec3 position;
uniform float r;
uniform float g;
uniform float b;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 transform;

out vec3 fragColor;

void main()
{
    fragColor = vec3(r, g, b);
    gl_Position = projection * view * transform * vec4(position, 1.0f);
}