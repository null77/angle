static float2 g_Corners[6] =
{
    float2(-1.0f,  1.0f),
    float2( 1.0f, -1.0f),
    float2(-1.0f, -1.0f),
    float2(-1.0f,  1.0f),
    float2( 1.0f,  1.0f),
    float2( 1.0f, -1.0f),
};

void VS_BlitDepthStencil(in uint id : SV_VertexID,
                         out float4 position : SV_Position,
                         out float2 texCoord : TEXCOORD0)
{
    float2 corner = g_Corners[id];
    position = float4(corner.x, corner.y, 0.0f, 1.0f);
    texCoord = float2((corner.x + 1.0f) * 0.5f, (-corner.y + 1.0f) * 0.5f);
}

Texture2DMS<float> Depth   : register(t0);

void PS_BlitDepthMS(in float4 position : SV_Position,
                    in float2 texCoord : TEXCOORD0,
                    out float depth : SV_Target0)
{
    // MS samplers must use Load
    uint width, height, samples;
    Depth.GetDimensions(width, height, samples);
    uint2 coord = uint2(texCoord.x * float(width), texCoord.y * float(height));
    depth = Depth.Load(coord, 0).r;
}

Texture2DMS<uint2> Stencil : register(t0);

void PS_BlitStencilMS(in float4 position : SV_Position,
                      in float2 texCoord : TEXCOORD0,
                      out uint stencil : SV_Target0)
{
    // MS samplers must use Load
    uint width, height, samples;
    Stencil.GetDimensions(width, height, samples);
    uint2 coord = uint2(texCoord.x * float(width), texCoord.y * float(height));
    stencil = Stencil.Load(coord, 0).g;
}
