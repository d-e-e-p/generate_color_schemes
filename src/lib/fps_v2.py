"""
mod from https://github.com/ziruiw-dev/farthest-point-sampling
"""

import numpy as np
import pudb
import math

class FPS:
    def __init__(self, pcd_xyz, distance_matrix, n_samples):
        self.n_samples = n_samples
        self.distance_matrix = distance_matrix
        self.pcd_xyz = pcd_xyz
        self.n_pts = pcd_xyz.shape[0]
        self.dim = pcd_xyz.shape[1]
        self.selected_pts_expanded = np.zeros(shape=(n_samples, 1, self.dim))
        self.remaining_pts = np.copy(pcd_xyz)

        self.grouping_radius = None
        self.dist_pts_to_selected = None  # Iteratively updated in step(). Finally re-used in group()
        self.labels = None
        self.selected_pts = None
        self.selected_idx = []
        self.n_selected_pts = 1
        self.current_distance = math.inf

    def run(self):
        num_runs = 1000
        res = []
        for run in range(num_runs):
            selected_pts = self.run_once(run)
            res.append([self.current_distance, selected_pts.tolist()])

        best_res = sorted(res, key=lambda x: (-x[0]))[0]
        return best_res[1]


    def run_once(self, run):
        # Random pick a start
        self.selected_idx = []
        self.start_idx = np.random.randint(low=0, high=self.n_pts - 1)
        self.selected_pts_expanded[0] = self.remaining_pts[self.start_idx]
        self.n_selected_pts = 1
        self.selected_idx.append(self.start_idx)
        return self.fit()

    def get_selected_pts(self):
        self.selected_pts = np.squeeze(self.selected_pts_expanded, axis=1)
        return self.selected_pts

    def step(self):
        if self.n_selected_pts < self.n_samples:
            res_selected_idx, distance = self.get_max_distance_point(self.selected_idx)
            self.selected_idx.append(res_selected_idx)
            pt = self.pcd_xyz[res_selected_idx]
            #print(f"point={self.remaining_pts.size} {self.n_selected_pts}/{self.n_samples} res_selected_idx = {res_selected_idx} distance={int(distance)} pt={pt} ")
            #pu.db
            self.selected_pts_expanded[self.n_selected_pts] = self.remaining_pts[res_selected_idx]

            self.n_selected_pts += 1
            self.current_distance=distance
        else:
            print("Got enough number samples")


    def fit(self):
        for _ in range(1, self.n_samples):
            self.step()
        return self.get_selected_pts()

    def group(self, radius):
        self.grouping_radius = radius   # the grouping radius is not actually used
        dists = self.dist_pts_to_selected

        # Ignore the "points"-"selected" relations if it's larger than the radius
        dists = np.where(dists > radius, dists+1000000*radius, dists)

        # Find the relation with the smallest distance.
        # NOTE: the smallest distance may still larger than the radius.
        self.labels = np.argmin(dists, axis=1)
        return self.labels

    def get_max_distance_point(self, pts_idx):
        #temp = np.linalg.norm(a - b, ord=2, axis=2)
        distance_slice = self.distance_matrix[:,pts_idx]
        distance_min = np.min(distance_slice, axis=1, keepdims=True)
        res_selected_idx = np.argmax(distance_min)
        return res_selected_idx, np.max(distance_min)
    


        for pl in b:
            for pt in pl:
                distances_to_target = self.distance_matrix[tuple(pt)]
                all_distances.append(distances_to_target)
                #print(f"pt = {pt} distances_to_target={distances_to_target}")

        res_distances = []
        for pt in a:
            distance_min = math.inf
            for distances_to_target in all_distances:
                distance = distances_to_target[tuple(pt)]
                if distance < distance_min:
                    distance_min = distance
                # ok record
            res_distances.append(distance_min)

        res_distances = np.array(res_distances)
        return res_distances
        #return temp


    def __distance__(self, a, b):
        return np.linalg.norm(a - b, ord=2, axis=2)
