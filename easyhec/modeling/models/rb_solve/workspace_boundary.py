import numpy as np
import trimesh
import torch
# from easyhec.utils.pn_utils import random_choice
# from easyhec.utils.vis3d_ext import Vis3D

def random_choice(x, size, dim=None, replace=True):
    if dim is None:
        assert len(x.shape) == 1
        n = x.shape[0]
        idxs = np.random.choice(n, size, replace)
        return x[idxs], idxs
    else:
        n = x.shape[dim]
        idxs = np.random.choice(n, size, replace)
        if isinstance(x, np.ndarray):
            swap_function = np.swapaxes
        elif isinstance(x, torch.Tensor):
            swap_function = torch.transpose
        else:
            raise TypeError()
        x_ = swap_function(x, 0, dim)
        x_ = x_[idxs]
        x_ = swap_function(x_, 0, dim)
        return x_, idxs
    
    
def get_workspace_boundary():
    # xmin, ymin, zmin, xmax, ymax, zmax = -0.2, -0.5, -0.5, 1.0, 0.5, 1.0
    xmin, ymin, zmin, xmax, ymax, zmax = -0.15, -0.35, -0.02, 0.8, 0.35, 1.05
    box = trimesh.primitives.Box(extents=[xmax - xmin, ymax - ymin, zmax - zmin])
    box.apply_translation([(xmax + xmin) / 2, (ymax + ymin) / 2, (zmax + zmin) / 2])
    pts_ws = box.sample(20000)

    pts_plane = np.zeros([20000, 3])
    pts_plane[:, 0] = np.random.uniform(-0.15, 0.8, size=20000)
    pts_plane[:, 1] = np.random.uniform(-0.35, 0.35, size=20000)
    pts_plane[:, 2] = 0
    norm = np.linalg.norm(pts_plane, axis=1)
    keep = norm > 0.3
    pts_plane = pts_plane[keep]
    pts_base = np.concatenate([pts_ws, pts_plane], axis=0)

    pts_base, _ = random_choice(pts_base, 10000, dim=0, replace=False)
    return pts_base

import viser 

def main():
    # vis3d = Vis3D(
    #     xyz_pattern=('x', 'y', 'z'),
    #     out_folder="dbg",
    #     sequence="model_env",
    # )
    pts_base = get_workspace_boundary()
    
    server = viser.ViserServer()
    server.scene.add_point_cloud(
        "pc", pts_base, colors=(255, 0, 0), point_size=0.003
    )
    import time 
    while True:
        time.sleep(1)
    # vis3d.add_point_cloud(pts_base)
    # vis3d.add_xarm(np.zeros(9))


if __name__ == '__main__':
    main()
