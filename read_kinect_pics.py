def ReadKinectPic(pathRGB, depthImage):

    DepthMap = [None] * (len(depthImage) * len(depthImage[0]))
    u = 0
    v= 0
    d = 0
    dmin = 2047
    dmax = 0

    n3DPoints = 0
    point3DArray= []

    # Get DepthImage file path

    pathDepth = pathRGB[:21]
    pathDepth = pathDepth + "-D.txt"

    fp = open(pathDepth, 'r')
    data = fp.read()
    data = data.split(' ')
    data = [i.replace('\n', '') for i in data]
    data.remove('')

    d_list = []
    for element in data:
        d_list.append(int(element))

    cnt = 0

    if fp:
     bOK = True

     for idxv in range(len(depthImage)):
        for idxu in range(len(depthImage[0])):


            d = d_list[cnt]

            if d == 2047:
                d = 0

            else:

                if d < dmin:
                    dmin = d

                if d > dmax:
                    dmax = d

            DepthMap[idxv * len(depthImage[0]) + idxu] = d


            point3DArray.append([idxu, idxv, d])

            cnt += 1

            if cnt==76801:
                break

    fp.close()
    n3DPoints = len(point3DArray)

    for idxv in range(len(depthImage)):
        for idxu in range(len(depthImage[0])):

            d = DepthMap[idxv * len(depthImage[0]) + idxu]

            if d != -1:
                d = ((d - dmin) * 254 / (dmax - dmin)) + 1
            else:
                d = 0

            depthImage[idxv][idxu] = d

    return point3DArray, n3DPoints, depthImage
