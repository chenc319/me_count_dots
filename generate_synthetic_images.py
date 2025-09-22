import numpy as np
from PIL import Image

def simulate_fluorescence_microscopy(image_size=512, cell_num_range=(20, 500), output_image='synthetic_image_00000001.png'):
    # Three channel base (RGB)
    img = np.zeros((image_size, image_size, 3), dtype=np.float32)
    mask = np.zeros((image_size, image_size), dtype=np.uint16)
    cell_count = np.random.randint(*cell_num_range)

    # Simulate nuclei (blue channel: DAPI-like)
    for i in range(1, cell_count // 3):
        x, y = np.random.randint(0, image_size, 2)
        radius = np.random.randint(8, 15)
        intensity = np.random.randint(180, 255)
        yy, xx = np.ogrid[:image_size, :image_size]
        circle = ((xx-x)**2 + (yy-y)**2) <= radius**2
        img[..., 2] += circle * intensity * np.exp(-((xx-x)**2 + (yy-y)**2) / (2 * (radius/2)**2))
        mask[circle] = i

    # Simulate glial/support cells (green channel)
    for i in range(cell_count // 3, 2 * cell_count // 3):
        x, y = np.random.randint(0, image_size, 2)
        axes = (np.random.randint(8, 15), np.random.randint(4, 10))
        angle = np.deg2rad(np.random.uniform(0, 360))
        intensity = np.random.randint(120, 210)
        yy, xx = np.ogrid[:image_size, :image_size]
        xc, yc = xx - x, yy - y
        x_rot = xc * np.cos(angle) + yc * np.sin(angle)
        y_rot = -xc * np.sin(angle) + yc * np.cos(angle)
        ellipse = ((x_rot / axes[0]) ** 2 + (y_rot / axes[1]) ** 2) <= 1
        img[..., 1] += ellipse * intensity * np.exp(-((x_rot) ** 2 + (y_rot) ** 2) / (2 * (axes[0]/2)**2))
        mask[ellipse] = i

    # Simulate axons/processes (red channel: filaments/tracks)
    for i in range(2 * cell_count // 3, cell_count):
        x, y = np.random.randint(0, image_size, 2)
        length = np.random.randint(20, 70)
        theta = np.random.uniform(0, 2 * np.pi)
        rr = np.linspace(0, length, num=length).astype(int)
        xx = np.clip(x + (rr * np.cos(theta)).astype(int), 0, image_size - 1)
        yy = np.clip(y + (rr * np.sin(theta)).astype(int), 0, image_size - 1)
        thickness = np.random.randint(2, 6)
        for j in range(len(rr)):
            img[max(yy[j]-thickness,0):min(yy[j]+thickness,image_size), max(xx[j]-thickness,0):min(xx[j]+thickness,image_size), 0] += np.random.randint(100,220)
            mask[max(yy[j]-thickness,0):min(yy[j]+thickness,image_size), max(xx[j]-thickness,0):min(xx[j]+thickness,image_size)] = i

    # Channel-specific noise/contrast
    img += np.random.normal(0, 15, img.shape)
    for c in range(3):
        img[...,c] = np.clip(img[...,c] * np.random.uniform(1.4, 2.2), 0, 255)
    img = np.clip(img, 0, 255).astype(np.uint8)

    Image.fromarray(img).save(output_image)
    Image.fromarray(mask).save(output_image.replace('.png','_mask.png'))

# Generate 50 images along fluorescence-style theme
for idx in range(1, 51):
    fname = f'synthetic_images/synthetic_image_{idx:08d}.png'
    simulate_fluorescence_microscopy(image_size=512, cell_num_range=(50, 500), output_image=fname)
