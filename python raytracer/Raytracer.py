import numpy as np
import sys

from ray import Ray
from scene import Scene
from sphere import Sphere
from light import Light
from point import Point

SMALL_NUMBER = 1e-8
OFFSET = 0.001
BIG_NUMBER = 1e8
MAX_DEPTH = 3

# PARSING FUNCTIONS

def parse_scene_file(fn):
    scene = Scene()
    sphere_list = []
    light_list = []
    with open(fn, 'r') as file:
        for line in file:
            words = line.split()
            if not words:
                continue 

            keyword = words[0].upper()

            if keyword == "NEAR":
                scene.near = float(words[1])
            elif keyword == "LEFT":
                scene.left = float(words[1])
            elif keyword == "RIGHT":
                scene.right = float(words[1])
            elif keyword == "BOTTOM":
                scene.bottom = float(words[1])
            elif keyword == "TOP":
                scene.top = float(words[1])
            elif keyword == "RES":
                scene.res_x = int(words[1])
                scene.res_y = int(words[2])
            elif keyword == "SPHERE":
                sphere_info = words[1:]
                sphere_list.append(sphere_info)
            elif keyword == "LIGHT":
                light_info = words[1:]
                light_list.append(light_info)
            elif keyword == "BACK":
                scene.background = [float(val) for val in words[1:]]
            elif keyword == "AMBIENT":
                scene.ambient = np.array([float(val) for val in words[1:]])
            elif keyword == "OUTPUT":
                scene.output = words[1]
                
    parse_spheres(scene,sphere_list)
    parse_lights(scene,light_list)
    
    return scene

def parse_spheres(scene, s_list):
    for sphere in s_list:
        name = sphere[0]
        posx, posy, posz, sclx, scly, sclz, r, g, b, ka, kd, ks, kr, n = (
            float(sphere[i]) for i in range(1, 15)
        )
        scene.spheres.append(Sphere(name, [posx, posy, posz], [sclx, scly, sclz], [r, g, b], ka, kd, ks, kr, n))

def parse_lights(scene,l_list):
    for light in l_list:
        name = light[0]
        posx, posy, posz, ir, ig, ib = (
            float(light[i]) for i in range(1, 7)
        )
        scene.lights.append(Light(name, [posx, posy, posz], [ir, ig, ib]))
        
# PPM FUNCTIONS
def save_image_p6(width, height, fname, pixels):
    max_val = 255

    print(f"Saving image {fname}: {width} x {height}")
    with open(fname, "wb") as fp:
        fp.write(b'P6\n')
        fp.write(f"{width} {height}\n".encode('utf-8'))
        fp.write(f"{max_val}\n".encode('utf-8'))

        for j in range(height):
            fp.write(pixels[j * width * 3: (j + 1) * width * 3])

# MATH

def normalize(v):
    return np.array(v / np.linalg.norm(v))

def reflect(v, n):
    return np.array(v - 2 * np.dot(v, n) * n)

def get_normal(point):
    sphere = point.sphere

    # normal in object coords
    local_normal = normalize((point.position - sphere.center) / sphere.scale)

    # normal in world coords
    world_normal = np.array([local_normal[i] / sphere.scale[i] for i in range(3)])

    return normalize(world_normal)


# RAYTRACING FUNCTIONS

def ray_through_pixel(eye, scene, W, H, r, c, u, v, n):
    
    # determine the direction of the ray from the eye
    ray_direction = -scene.near * n + W * ((2 * c / scene.res_x) - 1) * u - H * ((2 * r / scene.res_y) - 1) * v
    ray_direction = normalize(ray_direction)
    
    # set origin
    ray_origin = eye
    
    # create ray
    ray = Ray(ray_origin, ray_direction)

    return ray

def intersect_ray_with_object(ray, sphere):
    
    # inversely scale ray
    inv_scale = np.array([1.0 / s for s in sphere.scale])
    scaled_direction = ray.direction * inv_scale
    scaled_origin = (ray.origin - sphere.center) * inv_scale
    inv_ray = Ray(scaled_origin, scaled_direction)
    
    # Use inv ray to find intersection with unit sphere
    a = np.dot(inv_ray.direction, inv_ray.direction)
    b = 2.0 * np.dot(inv_ray.origin, inv_ray.direction)
    c = np.dot(inv_ray.origin, inv_ray.origin) - 1

    discriminant = b**2 - 4 * a * c

    if discriminant > 0:
        t1 = (-b - np.sqrt(discriminant)) / (2 * a)
        t2 = (-b + np.sqrt(discriminant)) / (2 * a)
        
        # Choose the closest intersection point in front of the ray
        # Use intersection in original ray to get intersection
        if t1 > 0 and t1 <= t2:
            intersection_point = ray.origin + t1 * ray.direction
            return Point(intersection_point,sphere)
        elif t2 > 0:
            intersection_point = ray.origin + t2 * ray.direction
            return Point(intersection_point,sphere)
    
    return None

def compute_closest_intersection(ray, spheres):
    closest_intersection = None
    # initalize the closest distance to a large number
    closest_distance = BIG_NUMBER

    # iterate through all spheres and intersect the ray with each sphere
    for sphere in spheres:
        point = intersect_ray_with_object(ray, sphere)

        # intersection is found
        if point is not None:
            distance = np.linalg.norm(point.position - ray.origin)
            # check if this distance to intersection is the shortest
            if distance < closest_distance:
                # if yes, set this to closest intersection
                closest_distance = distance
                closest_intersection = point
        
    # if no intersection is found, closest_intersection is empty
    return closest_intersection

def compute_shadow_ray(scene,eye,light, point, spheres):
    # initialize color to 0
    color = np.array([0.0,0.0,0.0])
    L = normalize(light.position - point.position) # direction to light
    
    # offset ray slightly
    ray_origin = point.position + OFFSET * L 
    shadow_ray = Ray(ray_origin, L) # shadow ray created
    
    # intersect the shadow ray with all spheres in the scene
    for sphere in spheres:
        intersection = intersect_ray_with_object(shadow_ray, sphere)
        if intersection is not None:
            # shadow ray hits object, point is in shadow
            return color # no color contribution (black)
            
    # no intersection exists, calculate illumination color
    color = np.array(illumination(eye,light, point, point.sphere))
    return color

def illumination(eye,light,point,sphere):
    L = normalize(light.position - point.position) # direction to light
    V = normalize(-point.position) # view vector
    N = get_normal(point) # normal
    R = normalize(reflect(-L,N)) # reflected vector

    # initialize diffuse and specular
    diffuse = np.array([0.0,0.0,0.0])
    specular = np.array([0.0,0.0,0.0])
    
    # calculate factors
    diffuse_factor = max(np.dot(N,L), 0)
    specular_factor = np.dot(R,V)
    if specular_factor > 0:
        specular_factor = pow(specular_factor, sphere.n)
    else:
        specular_factor = 0

    # Set r g b values of diffuse and specular
    for i in range(3):
        specular[i] = sphere.ks * specular_factor * light.intensity[i]    
        diffuse[i] = sphere.kd * sphere.color[i] * diffuse_factor * light.intensity[i]

    color = diffuse + specular # ambient is calculated in raytrace()
    
    return color

def compute_reflected_ray(ray, point):
    V = normalize(ray.origin - point.position)  # initial vector
    N = get_normal(point) # normal
    R = normalize(reflect(-V,N)) # reflected vector

    # get origin
    scaled_origin = np.array([0.0,0.0,0.0])
    for i in range(3):
        scaled_origin[i]= point.position[i] + R[i] / point.sphere.scale[i]
    offset_origin = scaled_origin + OFFSET * R
    
    # create reflected ray
    ref_ray = Ray(offset_origin, R)

    return ref_ray

def raytrace(eye,ray,scene):
    # cap ray recursion at MAX_DEPTH bounces
    if ray.depth > MAX_DEPTH:
        # max depth reached, return black
        return [0.0, 0.0, 0.0]
    else:
        ray.depth += 1 # increment depth
        P = compute_closest_intersection(ray,scene.spheres)
        
        if P is None: # no intersection found
            if (ray.depth < 2):
                # if it's the inital raytrace() call, return background
                return scene.background
            else:
                # this is for reflected color, return black
                return [0.0,0.0,0.0]
      
        # ambient calculation
        ambient = np.array(scene.ambient * P.sphere.color * P.sphere.ka)
        
        # diffuse and specular accumulation
        color_local = [0.0,0.0,0.0]
        # collect diffuse and specular according to each light in the scene
        for light in scene.lights:
            # check if sphere will be cut by img plane
            if P.position[2] >= -scene.near:
                # check if any lights exist that are between the sphere and the near plane
                if light.position[2] >= -scene.near:
                    # if yes, illuminate sphere with light
                    color_local += compute_shadow_ray(scene,eye,light, P,scene.spheres)
            else:
                # color as normal
                color_local += compute_shadow_ray(scene,eye,light, P,scene.spheres)

            
        # reflection color
        ref_ray = compute_reflected_ray(ray, P)
        ref_ray.depth = ray.depth
        # initialize reflected color
        color_reflect = [0.0,0.0,0.0]
        
        color_reflect = raytrace(eye, ref_ray, scene) # recursive call to accumulate color
        
        # combine ambient, diffuse, specular and reflected colors
        kre = P.sphere.kr
        color = [
            ambient [0] + color_local[0] + kre * color_reflect[0],
            ambient[1] + color_local[1] + kre * color_reflect[1],
            ambient[2] + color_local[2] + kre * color_reflect[2]
        ]
        
        color = [min(max(c, 0.0),1.0) for c in color] # 0 <= r,g,b <= 1
    
        return color

def main():
    
    # if no input file is given
    if len(sys.argv) != 2:
        print("Input file name") 
        return
    
    # get file name
    fn = sys.argv[1] 
    scene = parse_scene_file(fn)   
    
    # set image
    width = scene.res_x
    height = scene.res_y
    out_file = scene.output
    pixels = np.zeros((height, width, 3), dtype=np.uint8)
     
    # set eye coordinate system
    eye = [0.0,0.0,0.0]
    u = normalize(np.array([1.0, 0.0, 0.0]))  # X-axis unit vector
    v = normalize(np.array([0.0, 1.0, 0.0]))  # Y-axis unit vector
    n = normalize(np.array([0.0, 0.0, 1.0]))  # Z-axis unit vector    
    
    # set image plane
    image_width = abs(scene.right - scene.left)
    image_height = abs(scene.bottom - scene.top)
    W = int(image_width/2)
    H = int(image_height/2)
    
    # shoot rays from each pixel
    for c in range(scene.res_x):
        for r in range(scene.res_y):
            # get pixel ray
            ray = ray_through_pixel(eye, scene, W, H, r, c, u, v, n)
            # determine pixel color
            color = raytrace(eye, ray, scene)
            # color pixel
            pixels[r, c] = [int(c * 255) for c in color]

    # save ppm image
    save_image_p6(width, height, out_file, pixels.flatten())     

if __name__ == "__main__":
    main()