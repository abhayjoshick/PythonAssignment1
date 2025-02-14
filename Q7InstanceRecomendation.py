import pandas as pd

instanceTypes = ['nano', 'micro', 'small', 'medium', 'large', 'xlarge', '2xlarge', '4xlarge', '8xlarge', '16xlarge', '32xlarge']

def recommendedInstance(currEc2, currCPU):
    instance_type, instance_size = currEc2.split('.')

    currIdx = instanceTypes.index(instance_size)

    if currCPU < 20:
        
        if currIdx > 0:
            recommended = instanceTypes[currIdx - 1]
        else:
            recommended = instance_size  
        status = 'Underutilized'
    elif 20 <= currCPU <= 80:
        recommended = instance_size  
        status = 'Optimized'
    else:
        if currIdx < len(instanceTypes) - 1:
            recommended = instanceTypes[currIdx + 1]
        else:
            recommended = instance_size  
        status = 'Overutilized'
    
    recommended_ec2 = f"{instance_type}.{recommended}"
    return currEc2, currCPU, status, recommended_ec2

def genereateTable(currEc2, currCPU):
    recommendations = []
    recommendations.append(recommendedInstance(currEc2, currCPU))
    
    df = pd.DataFrame(recommendations, columns=['Current EC2', 'Current CPU (%)', 'Status', 'Recommended EC2'])
    df.index += 1 
    df.insert(0, 'Serial No.', df.index)  
    return df


currEc2 = input("Enter the current EC2 instance (e.g., t2.large): ")
currCPU = float(input("Enter the current CPU utilization (e.g., 20.5): "))

df = genereateTable(currEc2, currCPU)

print(df)
