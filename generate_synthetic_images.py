import numpy as np
from PIL import Image, ImageDraw

def gaussian_circle(image, center, radius, intensity):
    """ Draws an approximate blurred circle (Gaussian blob) in a NumPy array. """
    x0, y0 = center
    y, x = np.ogrid[:image.shape[0], :image.shape[1]]
    mask = (x - x0)**2 + (y - y0)**2 <= radius**2
    image[mask] += intensity * np.exp(-((x[mask] - x0)**2 + (y[mask] - y0)**2) / (2 * (radius/2.0)**2))

def generate_cells_pil(image_size=256, cells_range=(10,40),
                       radius_range=(7,25), intensity_range=(120,255),
                       output_image='synthetic_cells_pil.png',
                       output_mask='synthetic_cells_mask_pil.png'):
    img = np.zeros((image_size, image_size), dtype=np.float32)
    mask = np.zeros((image_size, image_size), dtype=np.uint8)
    num_cells = np.random.randint(*cells_range)
    for i in range(1, num_cells+1):
        x, y = np.random.randint(0, image_size, 2)
        radius = np.random.randint(*radius_range)
        intensity = np.random.randint(*intensity_range)
        gaussian_circle(img, (x, y), radius, intensity)
        yy, xx = np.ogrid[:image_size, :image_size]
        mask_area = (xx-x)**2 + (yy-y)**2 <= radius**2
        mask[mask_area] = i
    # Normalize image, clip and add noise & background shades
    img = np.clip(img + np.random.normal(5, 12, img.shape), 0, 255).astype(np.uint8)
    img = img + np.linspace(15, 80, image_size).astype(np.uint8)[:,None]
    # Save as PNG
    Image.fromarray(img).save(output_image)
    Image.fromarray(mask).save(output_mask)
    print(f"Saved: {output_image}, {output_mask}")

# Example usage—batch generation
for i in range(10):
    generate_cells_pil(output_image=f'synthetic_cells_pil_{i:03d}.png',
                       output_mask=f'synthetic_cells_mask_pil_{i:03d}.png')
