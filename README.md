# MoGraph Baker
 
For those pesky times when you’ve used a Mograph Cloner object as an assistant to create an animation and then realised that when you export it as an FBX none of the animation survives.

This Python plugin creates an "expanded" version of the Cloner (via current state to object) and then creates position, rotation and scale key frames every frame on the new hierarchy.

The original hierarchy is hidden and disabled, but is otherwise untouched.

Also works with MoGraph Voronoi Fractures.

At the moment it doesn't handle anything beyond the simplest use case, as that's all I needed it for, and I just wanted to see what was involved.

### Cloner with tank tread object, cloned along a spline: frame 0, offset 0%
![MoGraph cloner, object cloned along a spline, frame 0, offset 0%](/images/Screenshot-1.jpg)

### Cloner with tank tread object, cloned along a spline: frame 90, offset 5.88%
![MoGraph cloner, object cloned along a spline, frame 90, offset 5.88%](/images/Screenshot-2.jpg)

### Cloner hidden and disabled, new hierachy with individual position, rotation and scale keys on every frame of project timeline
![New hierarchy with position, scale and rotation keys on every frame](/images/Screenshot-3.jpg)

