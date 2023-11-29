#version 330

in vec3 frag_position;
in vec2 frag_texcoord;
in vec3 frag_normal;
out vec4 outColor;
uniform sampler2D sampler_tex;
uniform vec3 Kd;
uniform vec3 Ld;
uniform vec3 light_position;

void main()
{

    vec3 normal = normalize(frag_normal);
    vec3 to_light = light_position - frag_position;
    vec3 light_dir = normalize(to_light);
    float diff = max(dot(normal, light_dir), 0.0);

    if(diff <= 0.15){
        outColor = vec4(0.0, 0.0, 0.0, 1.0);
    }else{
        if(diff < 0.3){
            diff = 0.15;
        }else if(diff < 0.7){
            diff = 0.4;
        }else{
            diff = 0.8;
        }

        vec3 diffuse = Kd * Ld * diff;
        vec4 texel = texture(sampler_tex, frag_texcoord) * vec4(diffuse, 1.0);
        if (texel.a < 0.5)
            discard;
        outColor = texel;
    }
}