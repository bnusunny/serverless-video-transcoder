#!/bin/bash

# configure memory for 3 lambda functions: split_video, transcode_video, and merge_video. 
for controller_mem in 10240
do
    aws lambda update-function-configuration --function-name serverless-video-transcoder-ControllerFunction-4H37U0UQBXEX --memory-size $controller_mem > /dev/null

    for transcode_mem in {10240..1024..-1024}
    do
        aws lambda update-function-configuration --function-name serverless-video-transcoder-TranscodeVideoFunction-1R5VGY5KH83SN --memory-size $transcode_mem > /dev/null

        for merge_mem in 10240
        do
            aws lambda update-function-configuration --function-name serverless-video-transcoder-MergeVideoFunction-MR1AMOYTU4ZB --memory-size $merge_mem > /dev/null
            current_timestamp=`date +%s%3N`
            executionName=transcoder_$transcode_mem-controller_$controller_mem-merger_$merge_mem-$current_timestamp
            echo "start execution: $executionName"
            exeARN=`aws stepfunctions start-execution --state-machine-arn arn:aws:states:ap-northeast-1:373534280245:stateMachine:MainStateMachine-yxlzN716DXxR  --name $executionName --input file://event.json | jq -r .executionArn`
            echo "execution-arn: $exeARN"
            echo "execution-arn: $exeARN" >> result.txt
            while :
            do
                exeStatus=`aws stepfunctions describe-execution --execution-arn $exeARN | jq -r .status`
                if [ $exeStatus != 'RUNNING' ]
                then
                    echo "done: $exeStatus"
                    break
                fi
                sleep 30
                echo "running..."
            done
            startDate=`aws stepfunctions describe-execution --execution-arn $exeARN | jq -r .startDate`
            start=$(date -d $startDate +%s%3N)
            stopDate=`aws stepfunctions describe-execution --execution-arn $exeARN | jq -r .stopDate`
            end=$(date -d $stopDate +%s%3N)
            ((duration=($end-$start)))
            echo "Duration: $duration"
            echo "Duration: $duration" >> result.txt
            traceHeader=`aws stepfunctions describe-execution --execution-arn $exeARN | jq -r .traceHeader`
            echo "TraceHeader: $traceHeader"
            echo "TraceHeader: $traceHeader" >> result.txt
        done

    done

done