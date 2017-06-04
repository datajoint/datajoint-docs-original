# Part Tables

In many cases an entity in one relation is inseparably associated with a group of entities in another, forming a master-part relationship.  For example, an image segmentation has a set of images segments that are an intrinsic component of the segmentation entry. In this case, the two tables may be called `Segmentation` and `Segmentation.Segment`.

