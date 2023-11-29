#version 330

in vec3 frag_position;
in vec2 frag_texcoord;
in vec3 frag_normal;
out vec4 outColor;
uniform sampler2D sampler_tex;
uniform vec3 Kd_1;
uniform vec3 Ld_1;
uniform vec3 light_position_1;
uniform vec3 Kd_2;
uniform vec3 Ld_2;
uniform vec3 light_position_2;

void main()
{

    vec3 normal = normalize(frag_normal);
    vec3 to_light_1 = light_position_1 - frag_position;
    vec3 light_dir_1 = normalize(to_light_1);
    float diff_1 = max(dot(normal, light_dir_1), 0.0);

    vec3 to_light_2 = light_position_2 - frag_position;
    vec3 light_dir_2 = normalize(to_light_2);
    float diff_2 = max(dot(normal, light_dir_2), 0.0);
    
    vec3 diffuse = Kd_1 * Ld_1 * diff_1 + Kd_2 * Ld_2 * diff_2;

    vec4 texel = texture(sampler_tex, frag_texcoord) * vec4(diffuse, 1.0);

    if (texel.a < 0.5)
        discard;
    outColor = texel;
}