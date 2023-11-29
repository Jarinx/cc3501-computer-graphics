#version 330
in vec3 position;
uniform mat4 view_transform;
uniform float r;
uniform float g;
uniform float b;

out vec3 fragColor;

void main()
{
    gl_Position = view_transform * vec4(position, 1.0f);
    fragColor = vec3(r,g,b);
}